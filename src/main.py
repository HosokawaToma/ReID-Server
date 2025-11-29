import fastapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

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
from presentation.person_path import PresentationPersonPath
from applications.person_flow import ApplicationPersonFlow
from presentation.identify_person.search import PresentationIdentifyPersonSearch
from applications.identify_person.search import ApplicationIdentifyPersonSearch
from presentation.person_images import PresentationPersonImages
from applications.person_images import ApplicationPersonImages
from presentation.person.snapshot.create import PresentationPersonSnapshotCreate
from applications.person.snapshot.create import ApplicationPersonSnapshotCreate
from background.person.snapshot.feature_extraction import BackgroundPersonSnapshotFeatureExtraction
from background.person.snapshot.identify import BackgroundPersonSnapshotIdentify
from environment import EnvironmentHash
class ServerApp:
    def __init__(
        self,
        host: str,
        port: int,
        fastapi_app: fastapi.FastAPI,
        background_person_snapshot_feature_extraction: BackgroundPersonSnapshotFeatureExtraction,
        background_person_snapshot_identify: BackgroundPersonSnapshotIdentify,
        login_admin_client: PresentationAuthLoginAdminClient,
        login_camera_client: PresentationAuthLoginCameraClient,
        refresh_admin_client: PresentationAuthRefreshAdminClient,
        camera_clients_create: PresentationCameraClientsCreate,
        person_snapshot_create: PresentationPersonSnapshotCreate,
        rtc_connection: PresentationRtcConnection,
        rtc_ice_server: PresentationRtcIceServer,
        person_path: PresentationPersonPath,
        identify_person_search: PresentationIdentifyPersonSearch,
        person_images: PresentationPersonImages,
    ):
        self.host = host
        self.port = port
        self.fastapi_app = fastapi_app
        self.background_person_snapshot_feature_extraction = background_person_snapshot_feature_extraction
        self.background_person_snapshot_identify = background_person_snapshot_identify
        self.login_admin_client = login_admin_client
        self.login_camera_client = login_camera_client
        self.refresh_admin_client = refresh_admin_client
        self.camera_clients_create = camera_clients_create
        self.person_snapshot_create = person_snapshot_create
        self.rtc_connection = rtc_connection
        self.rtc_ice_server = rtc_ice_server
        self.person_path = person_path
        self.identify_person_search = identify_person_search
        self.person_images = person_images

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "ServerApp":
        environment_hash = EnvironmentHash(
            secret=environment.hash_key(),
        )
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
            background_person_snapshot_feature_extraction=BackgroundPersonSnapshotFeatureExtraction.create(
                environment=environment,
            ),
            background_person_snapshot_identify=BackgroundPersonSnapshotIdentify.create(
                environment=environment,
            ),
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
                    environment_hash=environment_hash,
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
                    environment_hash=environment_hash,
                )
            ),
            person_snapshot_create=PresentationPersonSnapshotCreate(
                auth=ApplicationAuthCameraClient.create(
                    environment_jwt=environment_jwt,
                    environment_postgresql=environment_postgresql,
                    environment_hash=environment_hash,
                ),
                application=ApplicationPersonSnapshotCreate.create(
                    environment=environment,
                ),
            ),
            rtc_connection=PresentationRtcConnection(
                application_auth=ApplicationAuthCameraClient.create(
                    environment_jwt=environment_jwt,
                    environment_postgresql=environment_postgresql,
                    environment_hash=environment_hash,
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
                    environment_hash=environment_hash,
                ),
                application=ApplicationRtcIceServer.create(
                    environment_coturn=environment_coturn,
                )
            ),
            person_path=PresentationPersonPath(
                application_person_flow=ApplicationPersonFlow.create(
                    environment_postgresql=environment_postgresql,
                ),
            ),
            identify_person_search=PresentationIdentifyPersonSearch(
                application_auth=ApplicationAuthAdminClient.create(
                    environment_jwt=environment_jwt,
                    environment_admin_client=environment_admin_client,
                ),
                application=ApplicationIdentifyPersonSearch.create(
                    environment_postgresql=environment_postgresql,
                    environment_storage=environment_storage,
                ),
            ),
            person_images=PresentationPersonImages(
                application_auth=ApplicationAuthAdminClient.create(
                    environment_jwt=environment_jwt,
                    environment_admin_client=environment_admin_client,
                ),
                application=ApplicationPersonImages.create(
                    environment_storage=environment_storage,
                    environment_postgresql=environment_postgresql
                ),
            ),
        )

    def run(self):
        self.fastapi_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.background_person_snapshot_feature_extraction.setup(self.fastapi_app)
        self.background_person_snapshot_identify.setup(self.fastapi_app)
        self.login_admin_client.setup(self.fastapi_app)
        self.login_camera_client.setup(self.fastapi_app)
        self.refresh_admin_client.setup(self.fastapi_app)
        self.camera_clients_create.setup(self.fastapi_app)
        self.person_snapshot_create.setup(self.fastapi_app)
        self.rtc_connection.setup(self.fastapi_app)
        self.rtc_ice_server.setup(self.fastapi_app)
        self.person_path.setup(self.fastapi_app)
        self.identify_person_search.setup(self.fastapi_app)
        self.person_images.setup(self.fastapi_app)
        uvicorn.run(self.fastapi_app, host=self.host, port=self.port)

if __name__ == "__main__":
    server_app = ServerApp.create(environment=Environment())
    server_app.run()
