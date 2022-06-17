from logging import exception
import MySQLdb

class dbHelper(object):
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "123456", "novel", charset='utf8')
        self.cursor = self.db.cursor()
        
    def insert(self, sql):
        try:
            self.cursor.execute(sql)
            id = self.db.insert_id()
            self.db.commit()
            return id
        except:
            self.db.rollback()
            return False
            
    def close(self):
        self.db.close()
