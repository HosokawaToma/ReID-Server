from presentation import PresentationBase, PresentationLogger, PresentationRequest, PresentationResponse
from applications.person.snapshot.refresh import ApplicationPersonSnapshotRefresh
from applications.person.snapshot.refresh import ApplicationPersonSnapshotRefreshParams
from applications.auth.admin_client import ApplicationAuthAdminClient
from presentation import PresentationTypeAuthorization
from environment import Environment
from entities.environment.jwt import EntityEnvironmentJwt
from entities.environment.admin_client import EntityEnvironmentAdminClient
from datetime import datetime

class PresentationPersonSnapshotRefreshRequest(PresentationRequest):
    after_timestamp: datetime | None = None
    before_timestamp: datetime | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None

class PresentationPersonSnapshotRefresh(PresentationBase):
    @property
    def router_path(self) -> str:
        return "/person/snapshot/refresh"

    @property
    def methods(self) -> list[str]:
        return ["POST"]

    tags = ["Person Snapshot"]
    summary = "Refresh person snapshots"
    description = "Refresh person snapshots"
    responses = {
        200: {
            "description": "Person snapshots refreshed",
        }
    }

    def __init__(
        self,
        logger: PresentationLogger,
        auth: ApplicationAuthAdminClient,
        application: ApplicationPersonSnapshotRefresh,
    ):
        super().__init__(logger)
        self.auth = auth
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "PresentationPersonSnapshotRefresh":
        return cls(
            logger=PresentationLogger(),
            auth=ApplicationAuthAdminClient.create(
                environment_jwt=EntityEnvironmentJwt(
                    secret_key=environment.jwt_secret_key(),
                    algorithm=environment.jwt_algorithm(),
                    expire_minutes=environment.jwt_expire_minutes(),
                ),
                environment_admin_client=EntityEnvironmentAdminClient(
                    id=environment.admin_client_id(),
                    password=environment.admin_client_password(),
                ),
            ),
            application=ApplicationPersonSnapshotRefresh.create(
                environment=environment,
            ),
        )

    async def handle(
        self,
        authorization: PresentationTypeAuthorization,
        request: PresentationPersonSnapshotRefreshRequest,
    ):
        try:
            self.auth.verify(authorization)
            await self.application.refresh(
                ApplicationPersonSnapshotRefreshParams(
                    after_timestamp=request.after_timestamp,
                    before_timestamp=request.before_timestamp,
                    camera_ids=request.camera_ids,
                    view_ids=request.view_ids,
                )
            )
            return PresentationResponse(status=200, content={"message": "Person snapshots refreshed"})
        except Exception as e:
            return PresentationResponse(status=500, content={"message": "Internal server error"})
