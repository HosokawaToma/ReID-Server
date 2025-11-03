import fastapi
from fastapi.responses import JSONResponse
from applications.login.camera_client import ApplicationLoginCameraClient
from presentation.login.camera_client.request import PresentationLoginCameraClientRequest


class PresentationLoginCameraClient():
    def __init__(
        self,
        application: ApplicationLoginCameraClient
        ):
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/login/camera_client", self.endpoint, methods=["POST"])

    def endpoint(self, request: PresentationLoginCameraClientRequest):
        try:
            token = self.application.login(request.camera_client_id, request.password)
            return JSONResponse(content={"token": token}, status_code=200)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
