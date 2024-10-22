import pymysql


class DatabaseConnection:
    def __init__(self):
        self.pwd = ""
        self.db = "tesca_forms"
        self.user = "root"
        self.port = 3306
        self.host = "localhost"

    def find_connection(self):
        conn = pymysql.connect(host=self.host,
                               port=self.port,
                               user=self.user,
                               password=self.pwd,
                               database=self.db)
        return conn, conn.cursor()
