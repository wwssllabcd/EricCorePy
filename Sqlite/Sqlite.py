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
        # type: tuple
        return c.fetchone()

    def close(self):
        self.clear_connect()

    # ex: "INSERT OR REPLACE INTO employees VALUES(1, 'John', 700, 'HR', 'Manager', '2017-01-04')"
    def insert(self, table, value):
        sql = 'INSERT OR REPLACE INTO ' + table + ' VALUES ' + value
        c = self.m_conn.cursor()
        c.execute(sql)
        self.m_conn.commit()


    # ex: "Select id, name from myTable where id = 12345"
    def query(self, table, field, whereVal):
        sql = f'SELECT {field} FROM {table} WHERE {whereVal}'
        c = self.m_conn.cursor()
        c.execute(sql)
        return c.fetchone()
        