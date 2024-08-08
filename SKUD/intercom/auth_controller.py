import json
import random as rnd
from datetime import datetime, timedelta

from ORM.database import DatabaseConnection
from ORM.loggers import Logger, VisitLogger
from ORM.queries.templates import condition_query
from general.singleton import Singleton
from remote.ui import Answer

class Tokens(Singleton):
    '''Класс для хранения токенов сессий'''
    def __init__(self) -> None:
        self.__randmax = 2**32
        self.__tokens = {}
        self.duration = timedelta(hours=15)

    def check_token(self, token: int, id: int) -> bool:
        '''Проверяет есть ли токен'''
        now = datetime.now()
        if id in self.__tokens:
            val = self.__tokens[id]
            return val[0] == token and val[1] - now <= self.duration
        return False         
    def add(self, id: str | int) -> int:
        '''Генерирует новый токен с `id`'''
        token = rnd.randint(0, self.__randmax)
        self.__tokens[id] = (token, datetime.now())
        return token
    
    def remove(self, id: str | int) -> bool:
        '''Удаление токена'''
        if id in self.__tokens:
            del self.__tokens[id]
            return True
        return False
        
class AuthenticationController:
    def __init__(self, remote_right: int, visits_db: VisitLogger, 
                       skud_db: DatabaseConnection, Debug: bool = False) -> None:
        self.visits_db = visits_db
        self.skud_db = skud_db
        self.remote_right = remote_right
        self.tokens = Tokens()

        self.Debug = Debug
        self.skud_db.establish_connection()
        sql = condition_query("access_rules", ["room"], f"right = {self.remote_right}")
        print(sql)
        self.remote_rooms = {row[0] for row in self.skud_db.execute_query(sql)}

    def verificator(self, data) -> Answer:  
        try:
            msg = json.loads(data)
            if msg['id'] in self.remote_rooms:
                sql = condition_query("entities", ["card"], 
                                     f"right = {self.remote_right} and card = {msg['key']}")
                card = self.skud_db.execute_query(sql) 

                #### DEBUG ####
                if self.Debug: print("data:", data, "card:", card)

                if len(card) == 1:
                    token = self.tokens.add(msg['id'])
                    return Answer(token, "")
                return Answer(0, "Invalid card")
            return Answer(0, "Invalid room")
        
        except BaseException as error:

            #### DEBUG ####
            if self.Debug: print("ERROR:", str(error))

            return Answer(0, str(error))
