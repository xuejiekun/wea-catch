# -*- coding:utf-8 -*-
import os
import sqlite3
import mysql.connector


class BaseSQL:

    def __init__(self, connector, **kwargs):
        self.conn = connector.connect(**kwargs)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

    def query(self, columns, table, condiction=None):
        columns = ','.join(columns)

        if condiction:
            self.cursor.execute('select {} from {} where {}'.format(columns, table, condiction))
        else:
            self.cursor.execute('select {} from {}'.format(columns, table))

    def insert(self, table, columns, values):
        columns = ','.join(columns)

        def str_preproc(s):
            if not s:
                return 'NULL'
            elif isinstance(s, str):
                return '"' + s + '"'
            else:
                return (str(s))
        values = ','.join(str_preproc(i) for i in values)
        # print(values)

        self.cursor.execute('insert into {}({}) values ({})'.format(table, columns, values))

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def _return_one(self):
        res = self.cursor.fetchone()
        if res is not None:
            res = res[0]
        return res


class SQLite3(BaseSQL):

    def __init__(self, **kwargs):
        super().__init__(sqlite3, **kwargs)
        self.cursor.execute('pragma foreign_keys = on')


class MySQL(BaseSQL):

    def __init__(self, **kwargs):
        # mysql.connector.paramstyle = 'qmark'
        super().__init__(mysql.connector, **kwargs)


if __name__ == '__main__':
    db = MySQL(user=os.getenv('mysqlu'), password=os.getenv('mysqlp'), host='localhost', database='wea')
    # db = SQLite3(r'H:\Python\web_catch\wea\data.db')

    db.query(['*'], 'address')
    for i in db.fetchall():
        print(i)

    db.close()
