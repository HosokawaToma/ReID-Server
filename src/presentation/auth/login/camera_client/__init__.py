import fastapi
from fastapi.responses import JSONResponse
from applications.auth.login.camera_client import ApplicationAuthLoginCameraClient
from presentation.auth.login.camera_client.request import PresentationAuthLoginCameraClientRequest


class PresentationAuthLoginCameraClient():
    def __init__(
        self,
        application: ApplicationAuthLoginCameraClient
        ):
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/auth/login/camera_client", self.endpoint, methods=["POST"])

    def endpoint(self, request: PresentationAuthLoginCameraClientRequest):
        try:
            token = self.application.login(request.camera_client_id, request.password)
            return JSONResponse(content={"token": token}, status_code=200)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
