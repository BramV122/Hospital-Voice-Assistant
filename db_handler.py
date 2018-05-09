#!/usr/bin/env python3

import pymysql

#HOST = "10.42.0.1"
HOST = "Localhost"
USER = "Voicekit"
PASSWD = "Voicekit"

class db_handler():

    def __init__(self):
        self._DB_Public = "VoiceKit"


    def findResponse(self, String):

        response = None

        try:
            self._db_public = pymysql.connect(HOST, USER, PASSWD, self._DB_Public)
            cursor = self._db_public.cursor()
        except pymysql.InternalError as e:
            print("Something went wrong with the database")
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))

        query = "SELECT Id, KeyWords FROM Responses"
        cursor.execute(query)

        answers = cursor.fetchall()
        responses = []

        for answer in answers:
            keywords = answer[1].split(";")
            foundKeys = False
            for keyword in keywords:
                if keyword in String:
                    foundKeys = True
                else:
                    foundKeys = False
                    break
            if foundKeys == True:
                responses.append(answer[0])

        if len(responses) > 1 or len(responses) == 0:
            print("no responses or multiple responses found")
        else:
            query = "SELECT Response FROM Responses WHERE ID = '%s'" % responses[0]
            cursor.execute(query)

            response = cursor.fetchall()[0][0]

        self._db_public.close()

        return response