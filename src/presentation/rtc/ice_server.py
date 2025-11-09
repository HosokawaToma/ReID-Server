import fastapi
from typing import Annotated
from fastapi import Header
from fastapi.responses import JSONResponse
from applications.rtc.ice_server import ApplicationRtcIceServer
from applications.auth.camera_client import ApplicationAuthCameraClient

class PresentationRtcIceServer:
    def __init__(
        self,
        application_auth: ApplicationAuthCameraClient,
        application: ApplicationRtcIceServer,
    ):
        self.application_auth = application_auth
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/rtc/ice_server", self.endpoint, methods=["GET"])

    async def endpoint(self, authorization: Annotated[str, Header()]):
        try:
            _, token = self.application_auth.parse(authorization)
            jwt_camera_client = self.application_auth.verify(token)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=401)
        try:
            return JSONResponse(
                content=self.application.generate(jwt_camera_client.id).to_dict(),
                status_code=200,
            )
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
