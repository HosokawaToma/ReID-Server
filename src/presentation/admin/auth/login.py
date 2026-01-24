from presentation.utils.base import PresentationUtilBase
from presentation.utils.factory import get_application
from logger import Logger
from presentation.utils.request import PresentationUtilRequest
from presentation.utils.request import PresentationUtilRequestBody
from presentation.utils.response import PresentationUtilJSONResponse
from applications.admin_client.auth.login import ApplicationAdminClientAuthLogin
from dto.admin_client.auth.credentials import DtoAdminClientAuthCredentials


class PresentationAdminAuthLoginRequestBody(PresentationUtilRequestBody):
    id: str
    password: str


class PresentationAdminAuthLogin(PresentationUtilBase):
    router_path = "/admin/auth/login"
    methods = ["POST"]
    tags = ["Admin Auth"]
    summary = "Login admin"
    description = "Login admin"
    responses = {
        200: {"description": "Login successful"},
        401: {"description": "Invalid credentials"},
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationAdminAuthLogin":
        return cls(
            logger=Logger("presentation_admin_auth_login"),
        )

    async def handle(
        self,
        request: PresentationUtilRequest,
        body: PresentationAdminAuthLoginRequestBody,
        application: ApplicationAdminClientAuthLogin = get_application(ApplicationAdminClientAuthLogin),
    ):
        result = application.login(
            DtoAdminClientAuthCredentials(
                id=body.id,
                password=body.password,
            ),
        )
        response = PresentationUtilJSONResponse(
            status=200, content={"token": result.token})
        response.set_refresh_token(refresh_token=result.refresh_token)
        return response
