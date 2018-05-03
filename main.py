#!/usr/bin/env python3
# Copyright 2017 Google Inc.

import logging
import platform
import sys
import threading

import aiy.assistant.auth_helpers
from aiy.assistant.library import Assistant
import aiy.audio
import aiy.voicehat
from google.assistant.library.event import EventType
from text_assistant import Text_Assistant
from db_handler import db_handler
from language_processing import language_processor

aiy.voicehat.get_status_ui().set_trigger_sound_wave('googlestart.wav')

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(message)s"
)

class MyAssistant(object):

    def __init__(self):
        self._task = threading.Thread(target=self._run_task)
        self._can_start_conversation = False
        self._assistant = None
        self._text_assistant = None
        self._language_processor = None

    def start(self):
        self._task.start()

    def _run_task(self):
        credentials = aiy.assistant.auth_helpers.get_assistant_credentials()
        with Assistant(credentials) as assistant:
            with Text_Assistant(credentials, aiy.i18n.get_language_code()) as textassistant:
                with language_processor(aiy.i18n.get_language_code()) as lang_processor:
                    self._assistant = assistant
                    self._text_assistant = textassistant
                    self._language_processor = lang_processor
                    for event in assistant.start():
                        self._process_event(event)

    def _process_event(self, event):
        status_ui = aiy.voicehat.get_status_ui()
        if event.type == EventType.ON_START_FINISHED:
            status_ui.status('ready')
            self._can_start_conversation = True
            aiy.voicehat.get_button().on_press(self._on_button_pressed)
            if sys.stdout.isatty():
                print('Say "OK, Google" or press the button, then speak.'
                      'Press ctrl+C to quit...')

        elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
            self._can_start_conversation = False
            status_ui .status('listening')

        elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED and event.args:
            print('You said: ', event.args['text'])
            text = event.args['text'].lower()

            keywords = self._language_processor.language_processing(text)
            print(keywords)

            db = db_handler()
            response = db.findResponse(text)

            if response:
                self._assistant.stop_conversation()
                self._text_assistant.assist("repeat after me " + response)

            # if 'ip address' in text:
            #     self._assistant.stop_conversation()
            #     ip_address = subprocess.check_output("hostname -I | cut -d' ' -f1", shell=True)
            #     self._text_assistant.assist("repeat after me my IP address is %s" % ip_address.decode('utf-8'))


        elif event.type == EventType.ON_END_OF_UTTERANCE:
            status_ui.status('thinking')

        elif (event.type == EventType.ON_CONVERSATION_TURN_FINISHED
              or event.type == EventType.ON_CONVERSATION_TURN_TIMEOUT
              or event.type == EventType.ON_NO_RESPONSE):
            status_ui.status('ready')
            self._can_start_conversation = True

        elif event.type == EventType.ON_ASSISTANT_ERROR and event.args and event.args['is_fatal']:
            sys.exit(1)

    def _on_button_pressed(self):
        if self._can_start_conversation:
            self._assistant.start_conversation()

def main():
    if platform.machine() == 'armv61':
        print('Cannot run hotword demo on Pi Zero!')
        exit(-1)
    MyAssistant().start()

if __name__ == '__main__':
    main()