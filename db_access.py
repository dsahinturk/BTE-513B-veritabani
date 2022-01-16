
import mysql.connector

config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 8889,
    'database': 'memberships',
    'raise_on_warnings': True
}


class DBConnection(object):

    def __init__(self):
        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor(dictionary=True)

    def close(self):
        self.cnx.close()

    def commit(self):
        self.cnx.commit()

    def __str__(self):
        return 'Database connection object'
