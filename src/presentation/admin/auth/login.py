from presentation import PresentationBase
from logger import Logger
from presentation import PresentationRequest
from presentation import PresentationRequestBody
from presentation import PresentationJSONResponse
from environment import Environment
from applications.admin_client.auth.login import ApplicationAdminClientAuthLogin
from applications.admin_client.auth.login import ApplicationAdminClientAuthLoginParams
from applications.admin_client.auth.login import ApplicationAdminClientAuthLoginInvalidCredentialsError

class PresentationAdminAuthLoginRequestBody(PresentationRequestBody):
    id: str
    password: str

class PresentationAdminAuthLogin(PresentationBase):
    router_path = "/admin/auth/login"
    methods = ["POST"]
    tags = ["Admin Auth"]
    summary = "Login admin"
    description = "Login admin"
    responses = {
        200: {"description": "Login successful"},
        401: {"description": "Invalid credentials"},
    }

    def __init__(self, logger: Logger, application: ApplicationAdminClientAuthLogin):
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "PresentationAdminAuthLogin":
        return cls(
            logger=Logger("admin_auth_login"),
            application=ApplicationAdminClientAuthLogin.create(environment=environment),
        )

    async def handle(self, request: PresentationRequest, body: PresentationAdminAuthLoginRequestBody):
        try:
            result = self.application.login(
                ApplicationAdminClientAuthLoginParams(
                    id=body.id,
                    password=body.password,
                ),
            )
        except ApplicationAdminClientAuthLoginInvalidCredentialsError as error:
            self.logger.error(error, request_id=request.get_request_id())
            return PresentationJSONResponse(status=401, content={
                "message": "Invalid credentials",
            })
        response = PresentationJSONResponse(status=200, content={"token": result.token})
        response.set_refresh_token(refresh_token=result.refresh_token)
        return response
