import fastapi
import uvicorn

from presentation.identify_person import PresentationIdentifyPerson
from applications.identify_person import ApplicationIdentifyPerson
from presentation.auth.login.admin_client import PresentationAuthLoginAdminClient
from presentation.auth.login.camera_client import PresentationAuthLoginCameraClient
from presentation.auth.refresh.admin_client import PresentationAuthRefreshAdminClient
from presentation.camera_clients.create import PresentationCameraClientsCreate
from presentation.rtc.connection import PresentationRtcConnection
from presentation.rtc.ice_server import PresentationRtcIceServer
from applications.camera_clients.create import ApplicationCameraClientsCreate
from applications.auth.admin_client import ApplicationAuthAdminClient
from applications.auth.camera_client import ApplicationAuthCameraClient
from applications.rtc.connection import ApplicationRtcConnection
from applications.rtc.ice_server import ApplicationRtcIceServer
from environment import Environment
from entities.environment.jwt import EntityEnvironmentJwt
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from entities.environment.storage import EntityEnvironmentStorage
from entities.environment.coturn import EntityEnvironmentCoturn
from entities.environment.admin_client import EntityEnvironmentAdminClient
from applications.identify_person.background.feature import ApplicationIdentifyPersonBackgroundFeature
from applications.identify_person.background.identify import ApplicationIdentifyPersonBackgroundIdentify


class ServerApp:
    def __init__(
        self,
        host: str,
        port: int,
        fastapi_app: fastapi.FastAPI,
        login_admin_client: PresentationAuthLoginAdminClient,
        login_camera_client: PresentationAuthLoginCameraClient,
        refresh_admin_client: PresentationAuthRefreshAdminClient,
        camera_clients_create: PresentationCameraClientsCreate,
        identify_person: PresentationIdentifyPerson,
        rtc_connection: PresentationRtcConnection,
        rtc_ice_server: PresentationRtcIceServer,
    ):
        self.host = host
        self.port = port
        self.fastapi_app = fastapi_app
        self.login_admin_client = login_admin_client
        self.login_camera_client = login_camera_client
        self.refresh_admin_client = refresh_admin_client
        self.camera_clients_create = camera_clients_create
        self.identify_person = identify_person
        self.rtc_connection = rtc_connection
        self.rtc_ice_server = rtc_ice_server

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "ServerApp":
        environment_jwt = EntityEnvironmentJwt(
            secret_key=environment.jwt_secret_key(),
            algorithm=environment.jwt_algorithm(),
            expire_minutes=environment.jwt_expire_minutes(),
        )
        environment_jwt_refresh = EntityEnvironmentJwt(
            secret_key=environment.jwt_refresh_secret_key(),
            algorithm=environment.jwt_refresh_algorithm(),
            expire_minutes=environment.jwt_refresh_expire_minutes(),
        )
        environment_postgresql = EntityEnvironmentPostgreSQL(
            host=environment.postgresql_host(),
            port=environment.postgresql_port(),
            user=environment.postgresql_user(),
            password=environment.postgresql_password(),
            database=environment.postgresql_database(),
        )
        environment_storage = EntityEnvironmentStorage(
            path=environment.storage_path(),
        )
        environment_coturn = EntityEnvironmentCoturn(
            host=environment.public_ip(),
            port=environment.coturn_secure_port(),
            username=environment.coturn_username(),
            credential=environment.coturn_credential(),
            secret=environment.coturn_secret(),
            ttl=environment.coturn_ttl(),
        )
        environment_admin_client = EntityEnvironmentAdminClient(
            id=environment.admin_client_id(),
            password=environment.admin_client_password(),
        )
        return cls(
            host=environment.host(),
            port=environment.port(),
            fastapi_app=fastapi.FastAPI(),
            login_admin_client=PresentationAuthLoginAdminClient(
                application_token=ApplicationAuthAdminClient.create(
                    environment_jwt=environment_jwt,
                    environment_admin_client=environment_admin_client,
                ),
                application_refresh_token=ApplicationAuthAdminClient.create(
                    environment_jwt=environment_jwt_refresh,
                    environment_admin_client=environment_admin_client,
                )
            ),
            login_camera_client=PresentationAuthLoginCameraClient(
                application_token=ApplicationAuthCameraClient.create(
                    environment_jwt=environment_jwt,
                    environment_postgresql=environment_postgresql,
                ),
            ),
            refresh_admin_client=PresentationAuthRefreshAdminClient(
                application_token=ApplicationAuthAdminClient.create(
                    environment_jwt=environment_jwt_refresh,
                    environment_admin_client=environment_admin_client,
                ),
                application_refresh_token=ApplicationAuthAdminClient.create(
                    environment_jwt=environment_jwt_refresh,
                    environment_admin_client=environment_admin_client,
                )
            ),
            camera_clients_create=PresentationCameraClientsCreate(
                application_auth=ApplicationAuthAdminClient.create(
                    environment_jwt=environment_jwt,
                    environment_admin_client=environment_admin_client,
                ),
                application=ApplicationCameraClientsCreate.create(
                    environment_postgresql=environment_postgresql,
                )
            ),
            identify_person=PresentationIdentifyPerson(
                application_auth=ApplicationAuthCameraClient.create(
                    environment_jwt=environment_jwt,
                    environment_postgresql=environment_postgresql,
                ),
                application=ApplicationIdentifyPerson.create(
                    environment_postgresql=environment_postgresql,
                    environment_storage=environment_storage,
                ),
                application_background_feature=ApplicationIdentifyPersonBackgroundFeature.create(
                    environment_postgresql=environment_postgresql,
                    environment_storage=environment_storage,
                ),
                application_background_identify=ApplicationIdentifyPersonBackgroundIdentify.create(
                    environment_postgresql=environment_postgresql,
                ),
            ),
            rtc_connection=PresentationRtcConnection(
                application_auth=ApplicationAuthCameraClient.create(
                    environment_jwt=environment_jwt,
                    environment_postgresql=environment_postgresql,
                ),
                application=ApplicationRtcConnection.create(
                    environment_coturn=environment_coturn,
                    environment_storage=environment_storage,
                )
            ),
            rtc_ice_server=PresentationRtcIceServer(
                application_auth=ApplicationAuthCameraClient.create(
                    environment_jwt=environment_jwt,
                    environment_postgresql=environment_postgresql,
                ),
                application=ApplicationRtcIceServer.create(
                    environment_coturn=environment_coturn,
                )
            ),
        )

    def run(self):
        self.login_admin_client.setup(self.fastapi_app)
        self.login_camera_client.setup(self.fastapi_app)
        self.refresh_admin_client.setup(self.fastapi_app)
        self.camera_clients_create.setup(self.fastapi_app)
        self.identify_person.setup(self.fastapi_app)
        self.rtc_connection.setup(self.fastapi_app)
        self.rtc_ice_server.setup(self.fastapi_app)
        uvicorn.run(self.fastapi_app, host=self.host, port=self.port)

if __name__ == "__main__":
    server_app = ServerApp.create(environment=Environment())
    server_app.run()
