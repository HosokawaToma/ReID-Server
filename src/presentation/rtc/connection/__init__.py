from typing import Annotated
import fastapi
from fastapi import Header
from fastapi.responses import JSONResponse
from applications.rtc.connection import ApplicationRtcConnection
from presentation.rtc.connection.request import PresentationRtcConnectionRequest
from entities.rtc.sdp import EntityRtcSdp

class PresentationRtcConnection:
    def __init__(self, application: ApplicationRtcConnection):
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/rtc/connection", self.endpoint, methods=["POST"])

    async def endpoint(self, authorization: Annotated[str, Header()], request: PresentationRtcConnectionRequest):
        try:
            camera_client = self.application.authenticate(authorization)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=401)
        try:
            sdp = await self.application.connect(camera_client, EntityRtcSdp(sdp=request.sdp, type=request.type))
            return JSONResponse(
                content={
                    "sdp": sdp.sdp,
                    "type": sdp.type,
                },
                status_code=200,
            )
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
