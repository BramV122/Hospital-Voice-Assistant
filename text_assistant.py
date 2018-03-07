import googlesamples.assistant.grpc.textinput
import google.auth.transport.grpc
import google.auth.transport.requests
import google.oauth2.credentials
import aiy.assistant.device_helpers as device_helpers

class Text_Assistant(googlesamples.assistant.grpc.textinput.SampleTextAssistant):

    def __init__(self, credentials):
        self._credentials = credentials
        self._model_id, self._device_id = device_helpers.get_ids_for_service(credentials)

        api_endpoint = 'embeddedassistant.googleapis.com'
        grpc_deadline = 60 * 3 + 5

        http_request = google.auth.transport.requests.Request()
        credentials.refresh(http_request)

        grpc_channel = google.auth.transport.grpc.secure_authorized_channel(credentials, http_request, api_endpoint)

        super().__init__('en-US', self._model_id, self._device_id, grpc_channel, grpc_deadline)