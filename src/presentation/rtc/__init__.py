import fastapi
from typing import Annotated
from fastapi import Header
from fastapi.responses import JSONResponse
from applications.rtc import ApplicationRtc
from presentation.rtc.request import PresentationRtcRequest

class PresentationRtc():
    def __init__(
        self,
        application: ApplicationRtc,
    ):
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/rtc/offer", self.endpoint_offer, methods=["POST"])

    async def endpoint_offer(self, authorization: Annotated[str, Header()], request: PresentationRtcRequest):
        try:
            client = self.application.authenticate(authorization)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=401)
        try:
            return await self.application.offer(client.id, request.sdp, request.type)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
