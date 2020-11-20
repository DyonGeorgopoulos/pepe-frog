import sqlite3
from sqlite3 import Error

class ConnectionHandler():
    def __init__(self):
        database = r"/home/mattermost-dev/py_remindme_bot/db/remindme.db"
        conn = self.create_connection(database)
        if conn is not None:
            self.connection = conn
    
    def create_connection(self,db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print(sqlite3.version)
        except Error as e:
            print(e)

        return conn
    
    def insertRecord(self,request):
        sql = ''' INSERT INTO reminders(userID,timeGenerated,timeToRemind,channelID,postID,username,triggerWord,teamDomain)
                  VALUES(?,?,?,?,?,?,?,?)
              '''
        curr = self.connection.cursor()
        cur.execute(sql,request)
        self.connection.commit()

        return cur.lastrowid
