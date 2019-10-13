import sqlite3

class SqliteUtility:
    def __init__(self):
        self.m_conn = None
        self.path = None

    def check_conn_null(self):
        if self.m_conn == None:
            raise Exception('m_conn==None')

    def open_database(self, path):
        self.m_conn = sqlite3.connect(path) 
        self.path = path
        return self.m_conn

    def execute(self, sqlcmd):
        self.check_conn_null()
        self.m_conn.cursor.execute(sqlcmd)

    def commit(self, sqlcmd):
        self.check_conn_null()
        self.m_conn.commit()

    def close(self):
        self.check_conn_null()
        self.m_conn.close()
