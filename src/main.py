import fastapi
import uvicorn


from presentation.identify_person import PresentationIdentifyPerson
from applications.identify_person import ApplicationIdentifyPerson
from presentation.login.camera_client import PresentationLoginCameraClient
from applications.login.camera_client import ApplicationLoginCameraClient
from presentation.rtc import PresentationRtc
from applications.rtc import ApplicationRtc
from environment import Environment

class ServerApp:
    def __init__(
        self,
        host: str,
        port: str,
        fastapi_app: fastapi.FastAPI,
        login_camera_client: PresentationLoginCameraClient,
        identify_person: PresentationIdentifyPerson,
        rtc: PresentationRtc,
    ):
        self.host = host
        self.port = port
        self.fastapi_app = fastapi_app
        self.login_camera_client = login_camera_client
        self.identify_person = identify_person
        self.rtc = rtc

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "ServerApp":
        return cls(
            host=environment.host(),
            port=environment.port(),
            fastapi_app=fastapi.FastAPI(),
            login_camera_client=PresentationLoginCameraClient(
                application=ApplicationLoginCameraClient.create(
                    jwt_secret_key=environment.jwt_secret_key(),
                    jwt_algorithm=environment.jwt_algorithm(),
                    mysql_engine_url=environment.mysql_engine_url(),
                )
            ),
            identify_person=PresentationIdentifyPerson(
                application=ApplicationIdentifyPerson.create(
                    jwt_secret_key=environment.jwt_secret_key(),
                    jwt_algorithm=environment.jwt_algorithm(),
                    mysql_engine_url=environment.mysql_engine_url(),
                    storage_path=environment.storage_path(),
                    chroma_host=environment.chroma_host(),
                    chroma_port=environment.chroma_port(),
                    chroma_secret_token=environment.chroma_secret_token(),
                )
            ),
            rtc=PresentationRtc(
                application=ApplicationRtc.create(
                    jwt_secret_key=environment.jwt_secret_key(),
                    jwt_algorithm=environment.jwt_algorithm(),
                    host=environment.rtc_host(),
                    port=environment.rtc_port(),
                    username=environment.rtc_username(),
                    password=environment.rtc_password(),
                )
            ),
        )

    def run(self):
        self.login_camera_client.setup(self.fastapi_app)
        self.identify_person.setup(self.fastapi_app)
        self.rtc.setup(self.fastapi_app)
        uvicorn.run(self.fastapi_app, host=self.host, port=self.port)

if __name__ == "__main__":
    server_app = ServerApp.create(environment=Environment())
    server_app.run()
