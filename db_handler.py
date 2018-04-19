#!/usr/bin/env python3

import pymysql

HOST = "10.42.0.1"
USER = "Voicekit"
PASSWD = "Voicekit"
DB = "VoiceKit"

class db_handler():

    def __init__(self):
        DB_Public = "VoiceKit"
        DB_Private = "Medical"


    def findResponse(self, KeyWords):

        try:
            self._db_public = pymysql.connect(HOST, USER, PASSWD, DB)
            cursor = self._db_public.cursor()
        except pymysql.InternalError as e:
            print("Something went wrong with the database")
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))

        query = "SELECT Response FROM Responses WHERE KeyWords LIKE '%s'" % KeyWords
        cursor.execute(query)

        answers = cursor.fetchall()
        if len(answers) == 1:
            response = answers[0]
            response = response[0]
        else:
            response = None
            print("query got more than 1 answer")

        self._db_public.close()

        return response