from presentation import PresentationBase, get_application
from logger import Logger
from presentation import PresentationRequest
from presentation import PresentationJSONResponse
from applications.admin_client.auth.token_refresh import ApplicationAdminClientAuthTokenRefresh
from applications.admin_client.auth.token_refresh import ApplicationAdminClientAuthTokenRefreshError
from dto.admin_client.auth.token import DtoAdminClientAuthToken


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

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationAdminAuthTokenRefresh":
        return cls(
            logger=Logger("presentation_admin_auth_token_refresh"),
        )

    async def handle(
        self,
        request: PresentationRequest,
        application: ApplicationAdminClientAuthTokenRefresh = get_application(ApplicationAdminClientAuthTokenRefresh),
    ):
        try:
            result = await self.run_sync(
                application.refresh,
                DtoAdminClientAuthToken(
                    token=request.get_refresh_token(),
                ),
            )
        except ApplicationAdminClientAuthTokenRefreshError as error:
            self.logger.api_response_info(request_id=request.get_request_id(), response_status_code=401)
            return PresentationJSONResponse(status=401, content={
                "message": "Invalid token",
            })
        response = PresentationJSONResponse(
            status=200, content={"token": result.token})
        response.set_refresh_token(refresh_token=result.refresh_token)
        return response
