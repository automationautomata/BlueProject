from json import JSONEncoder

class EntityView(JSONEncoder):
     def __init__(self, **kwargs) -> None:
        self.card = kwargs["card"]
        self.isSabotagedCard = kwargs["isSabotagedCard"]
        self.cardAddDate = kwargs["cardAddDate"]
        self.right = kwargs["right"]
        self.rightName = kwargs["rightName"]
        self.rightAddDate = kwargs["rightAddDate"]
        self.rightDelDate = kwargs["rightDelDate"]
        self.sid = kwargs["sid"]
        self.type = kwargs["type"]
        self.entityAddDate = kwargs["entityAddDate"]
        self.entityDelDate = kwargs["entityDelDate"]

class AccessRuleView(JSONEncoder):
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
