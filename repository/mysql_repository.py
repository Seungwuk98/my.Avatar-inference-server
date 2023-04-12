import pymysql
from repository.abc_repository import repository
from repository.sql.sql import *

class mysql_repository(repository):
    def __init__(self) -> None:
        self.db = pymysql.connect(
                    host = 'localhost',
                    port = 3306,
                    user = 'root',
                    passwd = 'root',
                    db='threeavatar',
                    charset='utf8'
                 )
        self.cursor = self.db.cursor()
        
    
    def get_body_url(self, body_num):
        self.db.ping(reconnect=True)
        try :
            self.cursor.execute(GET_BODY_URL, body_num)
            result = self.cursor.fetchone()
        except :
            raise '유효하지 않은 body number'
        return result[0]
    
    def get_hair_url(self, hair_num):
        self.db.ping(reconnect=True)
        try :
            self.cursor.execute(GET_HAIR_URL, hair_num)
            result = self.cursor.fetchone()
        except :
            raise '유효하지 않은 hair number'
        return result[0]

    def get_body_config(self, body_num):
        self.db.ping(reconnect=True)
        try :
            self.cursor.execute(GET_BODY_CONFIG, body_num)
            excute_result = self.cursor.fetchone()
            result = {'x':excute_result[0], 'y':excute_result[1], 'z':excute_result[2], 's':excute_result[3]}
        except :
            raise '유효하지 않은 body number'
        return result
    
    def get_hair_config(self, hair_num):
        self.db.ping(reconnect=True)
        try :
            self.cursor.execute(GET_HAIR_CONFIG, hair_num)
            excute_result = self.cursor.fetchone()
            result = {'x':excute_result[0], 'y':excute_result[1], 'z':excute_result[2], 's':excute_result[3]}
        except :
            raise '유효하지 않은 body number'
        return result

    