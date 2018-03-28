#!/usr/bin/env python3
"""Sample that implements a text client for the Google Assistant Service."""

from google.assistant.embedded.v1alpha2 import (
    embedded_assistant_pb2,
    embedded_assistant_pb2_grpc
)

import math
import array
import aiy.audio as audio
import googlesamples.assistant.grpc.assistant_helpers as assistant_helpers

ASSISTANT_API_ENDPOINT = 'embeddedassistant.googleapis.com'
DEFAULT_GRPC_DEADLINE = 60 * 3 + 5


class SampleTextAssistant(object):
    """Sample Assistant that supports text based conversations.
    Args:
      language_code: language for the conversation.
      device_model_id: identifier of the device model.
      device_id: identifier of the registered device instance.
      channel: authorized gRPC channel for connection to the
        Google Assistant API.
      deadline_sec: gRPC deadline in seconds for Google Assistant API call.
    """

    def __init__(self, language_code, device_model_id, device_id,
                 channel, deadline_sec):
        self.language_code = language_code
        self.device_model_id = device_model_id
        self.device_id = device_id
        self.conversation_state = None
        self.assistant = embedded_assistant_pb2_grpc.EmbeddedAssistantStub(
            channel
        )
        self.deadline = deadline_sec

    def __enter__(self):
        return self

    def __exit__(self, etype, e, traceback):
        if e:
            return False

    def assist(self, text_query):
        """Send a text request to the Assistant and playback the response.
        """
        def iter_assist_requests():
            dialog_state_in = embedded_assistant_pb2.DialogStateIn(
                language_code=self.language_code,
                conversation_state=b''
            )
            if self.conversation_state:
                dialog_state_in.conversation_state = self.conversation_state
            config = embedded_assistant_pb2.AssistConfig(
                audio_out_config=embedded_assistant_pb2.AudioOutConfig(
                    encoding='LINEAR16',
                    sample_rate_hertz=16000,
                    volume_percentage=80,
                ),
                dialog_state_in=dialog_state_in,
                device_config=embedded_assistant_pb2.DeviceConfig(
                    device_id=self.device_id,
                    device_model_id=self.device_model_id,
                ),
                text_query=text_query,
            )
            req = embedded_assistant_pb2.AssistRequest(config=config, audio_in=None)
            assistant_helpers.log_assist_request_without_audio(req)
            yield req

        def normalize_audio(buf, volume_percentage):
            scale = math.pow(2, 1.0*volume_percentage/100)-1
            arr = array.array('h', buf)
            for idx in range(0, len(arr)):
                arr[idx] = int(arr[idx]*scale)
            buf = arr.tostring()
            return buf

        display_text = None
        buffer = b''
        for resp in self.assistant.Assist(iter_assist_requests(),
                                          self.deadline):
            assistant_helpers.log_assist_response_without_audio(resp)
            if resp.audio_out.audio_data:
                if len(resp.audio_out.audio_data) > 0:
                    buffer = buffer + resp.audio_out.audio_data
            if resp.dialog_state_out.conversation_state:
                conversation_state = resp.dialog_state_out.conversation_state
                self.conversation_state = conversation_state
            if resp.dialog_state_out.supplemental_display_text:
                display_text = resp.dialog_state_out.supplemental_display_text
        buffer = normalize_audio(buffer, 80)
        audio.play_audio(buffer)
        return display_text
