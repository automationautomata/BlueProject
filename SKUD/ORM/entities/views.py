class EntityView:
     def __init__(self, card, isSabotagedCard, cardAddDate, 
                        right, rightName, rightAddDate, rightDelDate,
                        sid, type, entityAddDate, entityDelDate) -> None:
        self.card = card
        self.isSabotagedCard = isSabotagedCard
        self.cardAddDate = cardAddDate 
        self.right = right
        self.rightName = rightName
        self.rightAddDate = rightAddDate
        self.rightDelDate = rightDelDate
        self.sid = sid  
        self.type = type
        self.entityAddDate = entityAddDate
        self.entityDelDate = entityDelDate

class AccessRuleView:
     def __init__(self, room, roomName, roomAddDate, roomDeleDate,
                        right, rightName, rightAddDate, rightDelDate, 
                        ruleAddDate, ruleDelDate):
        self.room = room 
        self.roomName = roomName  
        self.roomAddDate = roomAddDate
        self.roomDeleDate = roomDeleDate 
        self.right = right
        self.rightName = rightName
        self.rightAddDate = rightAddDate
        self.rightDelDate = rightDelDate
        self.ruleAddDate = ruleAddDate
        self.ruleDelDate = ruleDelDate
