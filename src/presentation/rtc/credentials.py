import fastapi
from typing import Annotated
from fastapi import Header
from fastapi.responses import JSONResponse
from applications.rtc.credentials import ApplicationRtcCredentials

class PresentationRtcCredentials:
    def __init__(self, application: ApplicationRtcCredentials):
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/rtc/credentials", self.endpoint_credentials, methods=["POST"])

    async def endpoint_credentials(self, authorization: Annotated[str, Header()]):
        try:
            client = self.application.authenticate(authorization)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=401)
        try:
            return JSONResponse(content=self.application.generate_turn_ice_servers(client.id), status_code=200)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
