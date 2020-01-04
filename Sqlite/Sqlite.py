import sqlite3

class SqliteUtility:
    def clear_connect(self):
        if self.m_conn != None:
            self.m_conn.close()
        self.m_conn = None
        self.path = None

    def __init__(self):
        self.m_conn = None
        self.clear_connect()

    def open_database(self, path):
        if self.m_conn != None:
            if self.path == path:
                return self.m_conn

        self.m_conn = sqlite3.connect(path) 
        self.path = path
        return self.m_conn

    def execute(self, sqlcmd):
        c = self.m_conn.cursor()
        c.execute(sqlcmd)
        return c.fetchone()

    def commit(self, sqlcmd):
        self.m_conn.commit()

    def close(self):
        self.clear_connect()
