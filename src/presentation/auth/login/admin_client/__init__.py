import fastapi
from fastapi.responses import JSONResponse
from applications.auth.admin_client import ApplicationAuthAdminClient
from presentation.auth.login.admin_client.request import PresentationAuthLoginAdminClientRequest
from entities.admin_client import EntityAdminClient

class PresentationAuthLoginAdminClient():
    TOKEN_BODY_NAME = "token"
    SET_COOKIE_HEADER_NAME = "Set-Cookie"
    SET_COOKIE_HEADER_VALUE_FORMAT = "Set-Cookie: {token}; Secure; HttpOnly; SameSite=Strict; Path=/api/auth/refresh/admin_client; Max-Age=0"
    def __init__(
        self,
        application_token: ApplicationAuthAdminClient,
        application_refresh_token: ApplicationAuthAdminClient
    ):
        self.application_token = application_token
        self.application_refresh_token = application_refresh_token

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/auth/login/admin_client",
                          self.endpoint, methods=["POST"])

    def endpoint(self, request: PresentationAuthLoginAdminClientRequest):
        try:
            admin_client = self.application_token.login(
                id=request.admin_client_id,
                password=request.password
            )
            return JSONResponse(
                status_code=200,
                content={
                    self.TOKEN_BODY_NAME: self.application_token.generate(
                        admin_client.id
                    )
                },
                headers={
                    self.SET_COOKIE_HEADER_NAME: self.SET_COOKIE_HEADER_VALUE_FORMAT.format(
                        token=self.application_refresh_token.generate(
                            admin_client.id
                        )
                    )
                }
            )
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
