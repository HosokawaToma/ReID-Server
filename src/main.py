import fastapi
import uvicorn

from presentation.identify_person import PresentationIdentifyPerson
from applications.identify_person import ApplicationIdentifyPerson
from presentation.login.camera_client import PresentationLoginCameraClient
from applications.login.camera_client import ApplicationLoginCameraClient
from presentation.rtc import PresentationRtc
from applications.rtc import ApplicationRtc
from environment import Environment
from entities.environment.jwt import EntityEnvironmentJwt
from entities.environment.mysql import EntityEnvironmentMysql
from entities.environment.chroma import EntityEnvironmentChroma
from entities.environment.storage import EntityEnvironmentStorage
from entities.environment.coturn import EntityEnvironmentCoturn


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
        environment_jwt = EntityEnvironmentJwt(
            secret_key=environment.jwt_secret_key(),
            algorithm=environment.jwt_algorithm(),
        )
        environment_mysql = EntityEnvironmentMysql(
            host=environment.mysql_host(),
            port=environment.mysql_port(),
            user=environment.mysql_user(),
            password=environment.mysql_password(),
            database=environment.mysql_database(),
        )
        environment_chroma = EntityEnvironmentChroma(
            host=environment.chroma_host(),
            port=environment.chroma_port(),
            secret_token=environment.chroma_secret_token(),
        )
        environment_storage = EntityEnvironmentStorage(
            path=environment.storage_path(),
        )
        environment_coturn = EntityEnvironmentCoturn(
            host=environment.public_ip(),
            port=environment.coturn_secure_port(),
            username=environment.coturn_username(),
            password=environment.coturn_password(),
        )
        return cls(
            host=environment.host(),
            port=environment.port(),
            fastapi_app=fastapi.FastAPI(),
            login_camera_client=PresentationLoginCameraClient(
                application=ApplicationLoginCameraClient.create(
                    environment_jwt=environment_jwt,
                    environment_mysql=environment_mysql,
                )
            ),
            identify_person=PresentationIdentifyPerson(
                application=ApplicationIdentifyPerson.create(
                    environment_jwt=environment_jwt,
                    environment_mysql=environment_mysql,
                    environment_chroma=environment_chroma,
                    environment_storage=environment_storage,
                )
            ),
            rtc=PresentationRtc(
                application=ApplicationRtc.create(
                    environment_jwt=environment_jwt,
                    environment_coturn=environment_coturn,
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
