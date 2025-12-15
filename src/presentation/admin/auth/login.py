from presentation import PresentationBase
from presentation import PresentationLogger
from presentation import PresentationRequestBody
from presentation import PresentationJSONResponse
from environment import Environment
from applications.admin_client.auth.login import ApplicationAdminClientAuthLogin
from applications.admin_client.auth.login import ApplicationAdminClientAuthLoginParams

class PresentationAdminAuthLoginRequest(PresentationRequestBody):
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

    def __init__(self, logger: PresentationLogger, application: ApplicationAdminClientAuthLogin):
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "PresentationAdminAuthLogin":
        return cls(
            logger=PresentationLogger(),
            application=ApplicationAdminClientAuthLogin.create(environment=environment),
        )

    async def handle(self, request: PresentationAdminAuthLoginRequest):
        result = self.application.login(
            ApplicationAdminClientAuthLoginParams(
                id=request.id,
                password=request.password,
            ),
        )
        response = PresentationJSONResponse(status=200, content={"token": result.token})
        response.set_refresh_token(refresh_token=result.refresh_token)
        return response
