import textinput
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials
import aiy.assistant.device_helpers as device_helpers
import googlesamples.assistant.grpc.audio_helpers as audio_helpers

audio_sample_rate = audio_helpers.DEFAULT_AUDIO_SAMPLE_RATE
audio_sample_width = audio_helpers.DEFAULT_AUDIO_SAMPLE_WIDTH
audio_block_size = audio_helpers.DEFAULT_AUDIO_DEVICE_BLOCK_SIZE
audio_flush_size = audio_helpers.DEFAULT_AUDIO_DEVICE_FLUSH_SIZE
audio_iter_size = audio_helpers.DEFAULT_AUDIO_ITER_SIZE

class Text_Assistant(textinput.SampleTextAssistant):

    def __init__(self, credentials):
        self._credentials = credentials
        self._model_id, self._device_id = device_helpers.get_ids_for_service(credentials)

        api_endpoint = 'embeddedassistant.googleapis.com'
        grpc_deadline = 60 * 3 + 5

        http_request = google.auth.transport.requests.Request()
        credentials.refresh(http_request)

        grpc_channel = google.auth.transport.grpc.secure_authorized_channel(credentials, http_request, api_endpoint)

        audio_device = None
        audio_source = audio_device = (
            audio_device or audio_helpers.SoundDeviceStream(
                sample_rate=audio_sample_rate,
                sample_width=audio_sample_width,
                block_size=audio_block_size,
                flush_size=audio_flush_size
            )
        )
        audio_sink = audio_device = (
            audio_device or audio_helpers.SoundDeviceStream(
                sample_rate=audio_sample_rate,
                sample_width=audio_sample_width,
                block_size=audio_block_size,
                flush_size=audio_flush_size
            )
        )

        # Create conversation stream with the given audio source and sink.
        conversation_stream = audio_helpers.ConversationStream(
            source=audio_source,
            sink=audio_sink,
            iter_size=audio_iter_size,
            sample_width=audio_sample_width,
        )

        super().__init__('en-US', self._model_id, self._device_id, grpc_channel, grpc_deadline, conversation_stream)