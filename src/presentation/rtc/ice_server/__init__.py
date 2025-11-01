import fastapi
from typing import Annotated
from fastapi import Header
from fastapi.responses import JSONResponse
from applications.rtc.ice_server import ApplicationRtcIceServer

class PresentationRtcIceServer:
    def __init__(self, application: ApplicationRtcIceServer):
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/rtc/ice_server", self.endpoint, methods=["GET"])

    async def endpoint(self, authorization: Annotated[str, Header()]):
        try:
            self.application.authenticate(authorization)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=401)
        try:
            return JSONResponse(content=self.application.generate().to_dict(), status_code=200)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
