# -*- coding:utf-8 -*-
import os

from config import database_file, database_file_cd2


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
    database = 'sqlite:///{}'.format(database_file)
