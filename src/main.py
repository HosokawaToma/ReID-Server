import fastapi
import uvicorn

from presentation import Presentation
from application.environment import ApplicationEnvironment
from application.login import ApplicationLogin
from application.identify_person import ApplicationIdentifyPerson
from application.rtc import ApplicationRtc
from application import Application

class ServerApp:
    def __init__(
        self,
        fastapi_app: fastapi.FastAPI,
        presentation: Presentation
        ):
        self.fastapi_app = fastapi_app
        self.presentation = presentation

    def run(self):
        self.presentation.setup(self.fastapi_app)
        uvicorn.run(self.fastapi_app, host="0.0.0.0", port=8888)

if __name__ == "__main__":
    environment = ApplicationEnvironment()
    login = ApplicationLogin(
        environment.get_jwt_secret_key(),
        environment.get_jwt_algorithm()
    )
    identify_person = ApplicationIdentifyPerson()
    rtc = ApplicationRtc(
        environment.get_server_ip(),
        environment.get_turn_username(),
        environment.get_turn_password()
    )
    application = Application(login, identify_person, rtc)
    presentation = Presentation(application)
    fastapi_app = fastapi.FastAPI()
    server_app = ServerApp(fastapi_app, presentation)
    server_app.run()
