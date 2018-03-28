#!/usr/bin/env python3

import pymysql

HOST = "10.42.0.1"
USER = "Voicekit"
PASSWD = "Voicekit"
DB = "VoiceKit"

class db_handler():

    def __init__(self):

        try:
            self._db = pymysql.connect(HOST, USER, PASSWD, DB)
            self._cursor = self._db.cursor()
        except pymysql.InternalError as e:
            print("Something went wrong with the database")
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))

    def findResponse(self, KeyWords):

        query = "SELECT Response FROM Responses WHERE KeyWords LIKE '%s'" % KeyWords
        self._cursor.execute(query)

        list = self._cursor.fetchall()
        if len(list) == 1:
            response = list[0]
            response = response[0]
        else:
            response = None

        self._db.close()

        return response