# -*- coding:utf-8 -*-
import os


# mysql
class MySQLTest():
    user = os.getenv('mysqlu')
    password = os.getenv('mysqlp')
    database = 'mysql+mysqlconnector://{}:{}@localhost:3306/wea'.format(user, password)

# mssql
class MSSQLTest():
    user = os.getenv('mssqlu')
    password = os.getenv('mssqlp')
    database = 'mssql+pymssql://{}:{}@localhost/wea'.format(user, password)

# sqlite3
class SQLite3Test():
    def __init__(self, database_file):
        self.database_file = database_file
        self.database = 'sqlite:///{}'.format(self.database_file)
