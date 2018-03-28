#!/usr/bin/env python3

import pymysql

HOST = "10.42.0.1"
USER = "root"
PASSWD = "SG7nsx4U"
DB = "Voicekit"

class db_handler():

    def __init__(self):

        try:
            self._db = pymysql.connect(HOST, USER, PASSWD, DB)
            self._cursor = self._db.cursor()
        except:
            print("Something went wrong with the database")

    def findResponse(self, KeyWords):
        response = None

        query = "SELECT Response FROM Responses WHERE KeyWords LIKE %s" % KeyWords
        self._cursor.execute(query)

        response = self._cursor.fetchall()[0]

        self._db.close()

        return response