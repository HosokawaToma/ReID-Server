import fastapi
import uvicorn

from presentation.rtc import PresentationRtc
from application.environment import ApplicationEnvironment
from presentation.login import PresentationLogin
from presentation.identify_person import PresentationIdentifyPerson


class ServerApp:
    def __init__(self):
        self.application_environment = ApplicationEnvironment()
        self.fastapi_app = fastapi.FastAPI()
        self.presentation_login = PresentationLogin()
        self.presentation_rtc = PresentationRtc()
        self.application_identify_person = PresentationIdentifyPerson()
        self.presentation_login.setup(self.fastapi_app)
        self.presentation_rtc.setup(self.fastapi_app)
        self.application_identify_person.setup(self.fastapi_app)

    def run(self):
        uvicorn.run(self.fastapi_app, host="0.0.0.0", port=8888)


if __name__ == "__main__":
    app = ServerApp()
    app.run()
