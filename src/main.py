import fastapi
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from environment import Environment
from presentation.admin.auth.login import PresentationAdminAuthLogin
from presentation.admin.auth.token_refresh import PresentationAdminAuthTokenRefresh
from presentation.person.snapshot.create import PresentationPersonSnapshotCreate
from presentation.person.snapshot.refresh import PresentationPersonSnapshotRefresh
from presentation.person.snapshot.search import PresentationPersonSnapshotSearch
from presentation.person.flow.search import PresentationPersonFlowSearch
from presentation.person.flow.weight.search import PresentationPersonFlowWeightSearch
from presentation.person.snapshot.image.search import PresentationPersonSnapshotImageSearch
from presentation.camera_frame.search import PresentationCameraFrameSearch
from presentation.camera_frame.image.search import PresentationCameraFrameImageSearch
from presentation import PresentationExceptionHandler, PresentationMiddleware
from logger import Logger

class ServerApp:
    def __init__(
        self,
        app_host: str,
        app_port: int,
        fastapi_app: fastapi.FastAPI,
        admin_auth_login: PresentationAdminAuthLogin,
        admin_auth_token_refresh: PresentationAdminAuthTokenRefresh,
        person_snapshot_create: PresentationPersonSnapshotCreate,
        person_snapshot_refresh: PresentationPersonSnapshotRefresh,
        person_snapshot_search: PresentationPersonSnapshotSearch,
        person_flow_search: PresentationPersonFlowSearch,
        person_flow_weight_search: PresentationPersonFlowWeightSearch,
        person_snapshot_image_search: PresentationPersonSnapshotImageSearch,
        camera_frame_search: PresentationCameraFrameSearch,
        camera_frame_image_search: PresentationCameraFrameImageSearch,
        presentation_exception_handler: PresentationExceptionHandler,
    ):
        self.app_host = app_host
        self.app_port = app_port
        self.fastapi_app = fastapi_app
        self.admin_auth_login = admin_auth_login
        self.admin_auth_token_refresh = admin_auth_token_refresh
        self.person_snapshot_create = person_snapshot_create
        self.person_snapshot_refresh = person_snapshot_refresh
        self.person_snapshot_search = person_snapshot_search
        self.person_flow_search = person_flow_search
        self.person_flow_weight_search = person_flow_weight_search
        self.person_snapshot_image_search = person_snapshot_image_search
        self.camera_frame_search = camera_frame_search
        self.camera_frame_image_search = camera_frame_image_search
        self.presentation_exception_handler = presentation_exception_handler

    @classmethod
    def create(
        cls,
        environment: Environment,
    ) -> "ServerApp":
        return cls(
            app_host=environment.app_host,
            app_port=environment.app_port,
            fastapi_app=fastapi.FastAPI(
                servers=[{"url": "/api/v1"}],
                root_path="/api/v1"
            ),
            admin_auth_login=PresentationAdminAuthLogin.create(),
            admin_auth_token_refresh=PresentationAdminAuthTokenRefresh.create(),
            person_snapshot_create=PresentationPersonSnapshotCreate.create(),
            person_snapshot_refresh=PresentationPersonSnapshotRefresh.create(),
            person_snapshot_search=PresentationPersonSnapshotSearch.create(),
            person_flow_search=PresentationPersonFlowSearch.create(),
            person_flow_weight_search=PresentationPersonFlowWeightSearch.create(),
            person_snapshot_image_search=PresentationPersonSnapshotImageSearch.create(),
            camera_frame_search=PresentationCameraFrameSearch.create(),
            camera_frame_image_search=PresentationCameraFrameImageSearch.create(),
            presentation_exception_handler=PresentationExceptionHandler.create(),
        )

    def run(self):
        self.fastapi_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self.fastapi_app.add_middleware(
            PresentationMiddleware,
            logger=Logger("presentation_middleware"),
        )
        self.admin_auth_login.setup(self.fastapi_app)
        self.admin_auth_token_refresh.setup(self.fastapi_app)
        self.person_snapshot_create.setup(self.fastapi_app)
        self.person_snapshot_refresh.setup(self.fastapi_app)
        self.person_snapshot_search.setup(self.fastapi_app)
        self.person_flow_search.setup(self.fastapi_app)
        self.person_flow_weight_search.setup(self.fastapi_app)
        self.person_snapshot_image_search.setup(self.fastapi_app)
        self.camera_frame_search.setup(self.fastapi_app)
        self.camera_frame_image_search.setup(self.fastapi_app)
        self.presentation_exception_handler.setup(self.fastapi_app)
        uvicorn.run(self.fastapi_app, host=self.app_host, port=self.app_port)

if __name__ == "__main__":
    server_app = ServerApp.create(environment=Environment())
    server_app.run()
