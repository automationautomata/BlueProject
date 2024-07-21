-------------------------TABLES-------------------------
CREATE TABLE cards (
    id VARCHAR(4) PRIMARY KEY,
    isSabotaged VARCHAR(1) NOT NULL,
    date_time TEXT NOT NULL
);
-- 0 - не саботирована, 1 - саботирована 
CREATE TABLE rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date_time TEXT NOT NULL
);
CREATE TABLE rights (
    id INTEGER NOT NULL AUTOINCREMENT,
    name TEXT NOT NULL,
    date_time_begin TEXT NOT NULL,
    date_time_end TEXT NOT NULL
);
CREATE TABLE access_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    right INTEGER NOT NULL,
    room INTEGER NOT NULL,
    date_time_begin TEXT NOT NULL,
    date_time_end TEXT NOT NULL,
    FOREIGN KEY(room) REFERENCES rooms(id),
    FOREIGN KEY(right) REFERENCES rights(id),
    UNIQUE(right, room)
);
CREATE TABLE entities (
    card VARCHAR(4),
    sid INTEGER PRIMARY KEY,
    type VARCHAR(1) NOT NULL,
    right INTEGER NOT NULL,
    date_time_begin TEXT NOT NULL,
    date_time_end TEXT NOT NULL,
    FOREIGN KEY(card) REFERENCES cards(id),
    FOREIGN KEY(right) REFERENCES rights(id)
);
-------------------------VIEWES---------------------------

CREATE VIEW entities_view 
AS select card, 
          isSabotaged as isSabotagedCard,  
          card.date_time as cardAddDate, 
          right, 
          right.name as rightName, 
          right.date_time_begin as rightAddDate,
          right.date_time_end as rightDelDate, 
          sid,
          type,
          date_time_begin as entityAddDate,
          date_time_end as entityDelDate
            from entities inner join cards on cards.id = entities.card    
                        inner join rights on entities.right = rights.right

CREATE VIEW access_rules_view 
AS select room, 
          room.name as roomName,  
          room.date_time_begin as roomAddDate, 
          room.date_time_end as roomDeleDate, 
          right, 
          right.name as rightName, 
          right.date_time_begin as rightAddDate,
          right.date_time_end as rightDelDate, 
          date_time_begin as ruleAddDate,
          date_time_end as ruleDelDate
            from entities inner join rooms on room.id = access_rules.room    
                        inner join rights on access_rules.right = rights.right


-------------------------TRIGGERS-------------------------
-- Можно ли добавлять в таблицу записи с правом, которому в access_rules
-- сопоставлены все записи с заполненным полем date_time_end ????
CREATE TRIGGER entities_check_card_upd
BEFORE UPDATE OF card ON entities
BEGIN
    SELECT RAISE(ABORT, 'CARD IS SABOTAGED') 
        WHERE 0 < SELECT SUM(e.isSabotaged) 
                        from new inner join cards 
                            on new.card = cards.id AS e;
END;

CREATE TRIGGER entities_check_right_upd
BEFORE UPDATE OF right ON entities
BEGIN
    SELECT RAISE(ABORT, 'RIGHT DATE ENDS DOES NOT CORRECT') 
        WHERE NOT EXISTS(SELECT * from new inner join cards 
                                on new.right = rights.id 
                                    WHERE rights.date_time_end = '');
END;


CREATE TRIGGER prevent_entities_insert_error
INSERT INSERT ON entities
BEGIN
    SELECT RAISE(ABORT, 'CARD IS SABOTAGED') 
        WHERE 0 < (SELECT SUM(e.isSabotaged) 
                        from NEW inner join cards 
                            on NEW.card = cards.id AS e) 

    SELECT RAISE(ABORT, 'RIGHT DATE END DOES NOT CORRECT') 
        WHERE NOT EXISTS(SELECT * from new inner join cards 
                                on NEW.right = rights.id 
                                    WHERE rights.date_time_end = '');
END;

CREATE TRIGGER handle_delete_entities 
INSTEAD OF DELETE ON entities
BEGIN
    UPDATE entities SET date_time_end=DATETIME('NOW')
        WHERE id=NEW.id;
END;

CREATE TRIGGER handle_delete_access_rules 
INSTEAD OF DELETE ON access_rules
BEGIN
    SELECT RAISE(ABORT, 'RIGHT WAS DELETED')
        WHERE NOT EXISTS(SELECT * from new inner join rights 
                                    on NEW.right = rights.id 
                                        WHERE rights.date_time_end = '');

    UPDATE access_rules SET date_time_end=DATETIME('NOW')
        WHERE id=NEW.id;
END;

CREATE TRIGGER handle_delete_rights INSTEAD OF DELETE ON rights
BEGIN
    UPDATE access_rules SET date_time_end=DATETIME('NOW')
        WHERE right=NEW.id;

    UPDATE rights SET date_time_end=DATETIME('NOW')
        WHERE id=NEW.id AND date_time_end='';
END;

