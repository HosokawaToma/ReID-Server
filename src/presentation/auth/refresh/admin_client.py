import fastapi
from applications.auth.admin_client import ApplicationAuthAdminClient
from typing import Annotated
from fastapi import Header
from fastapi.responses import JSONResponse

class PresentationAuthRefreshAdminClient:
    TOKEN_BODY_NAME = "token"
    SET_COOKIE_HEADER_NAME = "Set-Cookie"
    SET_COOKIE_HEADER_VALUE_FORMAT = "Set-Cookie: {token}; Secure; HttpOnly; SameSite=Strict; Path=/api/auth/refresh/admin_client; Max-Age=0"

    def __init__(
        self, application_token: ApplicationAuthAdminClient, application_refresh_token: ApplicationAuthAdminClient):
        self.application_token = application_token
        self.application_refresh_token = application_refresh_token

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/auth/refresh/admin_client", self.endpoint, methods=["POST"])

    def endpoint(self, authorization: Annotated[str, Header()]):
        try:
            admin_client = self.application_token.verify(authorization)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=401)
        try:
            return JSONResponse(
                content={
                    self.TOKEN_BODY_NAME: self.application_token.generate(
                        admin_client.id
                    )
                },
                headers={
                    self.SET_COOKIE_HEADER_NAME: self.SET_COOKIE_HEADER_VALUE_FORMAT.format(
                        token=self.application_refresh_token.generate(admin_client.id)
                    )
                }
            )
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=500)
