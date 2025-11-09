import fastapi
from applications.auth.camera_client import ApplicationAuthCameraClient
from typing import Annotated
from fastapi import Header
from fastapi.responses import JSONResponse


class PresentationAuthRefreshCameraClient:
    TOKEN_BODY_NAME = "token"
    SET_COOKIE_HEADER_NAME = "Set-Cookie"
    SET_COOKIE_HEADER_VALUE_FORMAT = "Set-Cookie: {token}; Secure; HttpOnly; SameSite=Strict; Path=/api/auth/refresh/camera_client; Max-Age=0"

    def __init__(
            self, application_token: ApplicationAuthCameraClient, application_refresh_token: ApplicationAuthCameraClient):
        self.application_token = application_token
        self.application_refresh_token = application_refresh_token

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/auth/refresh/camera_client",
                          self.endpoint, methods=["POST"])

    def endpoint(self, authorization: Annotated[str, Header()]):
        try:
            camera_client = self.application_token.verify(authorization)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=401)
        try:
            return JSONResponse(
                content={
                    self.TOKEN_BODY_NAME: self.application_token.generate(
                        camera_client.id,
                        camera_client.camera_id,
                        camera_client.view_id
                    )
                },
                headers={
                    self.SET_COOKIE_HEADER_NAME: self.SET_COOKIE_HEADER_VALUE_FORMAT.format(
                        token=self.application_refresh_token.generate(
                            camera_client.id,
                            camera_client.camera_id,
                            camera_client.view_id
                        )
                    )
                }
            )
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=500)
