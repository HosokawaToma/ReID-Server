from presentation import PresentationBase
from presentation import PresentationLogger
from presentation import PresentationRequest
from presentation import PresentationJSONResponse
from environment import Environment
from applications.admin_client.auth.token_refresh import ApplicationAdminClientAuthTokenRefresh
from applications.admin_client.auth.token_refresh import ApplicationAdminClientAuthTokenRefreshParams
from applications.admin_client.auth.token_refresh import ApplicationAdminClientAuthTokenRefreshError

class PresentationAdminAuthTokenRefresh(PresentationBase):
    router_path = "/admin/auth/token/refresh"
    methods = ["POST"]
    tags = ["Admin Auth"]
    summary = "Refresh admin token"
    description = "Refresh admin token"
    responses = {
        200: {"description": "Token refreshed"},
        401: {"description": "Invalid token"},
    }

    def __init__(self, logger: PresentationLogger, application: ApplicationAdminClientAuthTokenRefresh):
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "PresentationAdminAuthTokenRefresh":
        return cls(
            logger=PresentationLogger(),
            application=ApplicationAdminClientAuthTokenRefresh.create(environment=environment),
        )

    async def handle(self, request: PresentationRequest):
        try:
            result = self.application.refresh(
                ApplicationAdminClientAuthTokenRefreshParams(
                    refresh_token=request.get_refresh_token(),
                ),
            )
        except ApplicationAdminClientAuthTokenRefreshError as error:
            self.logger.error(error.message)
            return PresentationJSONResponse(status=401, content={
                "message": "Invalid token",
            })
        response = PresentationJSONResponse(status=200, content={"token": result.token})
        response.set_refresh_token(refresh_token=result.refresh_token)
        return response
