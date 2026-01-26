from presentation.utils.base import PresentationUtilBase
from presentation.utils.factory import get_application
from logger import Logger
from presentation.utils.request import PresentationUtilRequest
from presentation.utils.response import PresentationUtilJSONResponse
from applications.admin_client.auth.token_refresh import ApplicationAdminClientAuthTokenRefresh
from dto.admin_client.auth.token import DtoAdminClientAuthToken


class PresentationAdminAuthTokenRefresh(PresentationUtilBase):
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
        request: PresentationUtilRequest,
        application: ApplicationAdminClientAuthTokenRefresh = get_application(
            ApplicationAdminClientAuthTokenRefresh),
    ):
        result = application.refresh(
            DtoAdminClientAuthToken(
                token=request.cookies.get("refresh_token", ""),
            ),
        )
        response = PresentationUtilJSONResponse(
            status=200, content={"token": result.token})
        response.set_refresh_token(refresh_token=result.refresh_token)
        return response
