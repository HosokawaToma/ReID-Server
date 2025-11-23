import fastapi
from fastapi.responses import JSONResponse
from applications.auth.camera_client import ApplicationAuthCameraClient
from presentation.auth.login.camera_client.request import PresentationAuthLoginCameraClientRequest
from applications.auth.camera_client import ApplicationAuthLoginCameraClientParams
class PresentationAuthLoginCameraClient():
    TOKEN_BODY_NAME = "token"

    def __init__(
        self,
        application_token: ApplicationAuthCameraClient,
        ):
        self.application_token = application_token

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/auth/login/camera_client", self.endpoint, methods=["POST"])

    def endpoint(self, request: PresentationAuthLoginCameraClientRequest):
        try:
            camera_client = self.application_token.login(
                ApplicationAuthLoginCameraClientParams(
                    id=request.camera_client_id,
                    password=request.password
                )
            )
            return JSONResponse(
                status_code=200,
                content={
                    self.TOKEN_BODY_NAME: self.application_token.generate(
                        camera_client.id,
                        camera_client.camera_id,
                        camera_client.view_id
                    )
                },
            )
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
