import fastapi
from fastapi.responses import JSONResponse
from applications.auth.camera_client import ApplicationAuthCameraClient
from applications.identify_person import ApplicationIdentifyPerson
from typing import Annotated
from fastapi import Header

class PresentationIdentifyPersonSearch:
    def __init__(self, application_auth: ApplicationAuthCameraClient, application: ApplicationIdentifyPerson):
        self.application_auth = application_auth
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/identify_person/search", self.endpoint, methods=["POST"])

    async def endpoint(self, authorization: Annotated[str, Header()]):
        try:
            token = self.application_auth.parse(authorization)
            camera_client = self.application_auth.verify(token)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=401)
        return JSONResponse(content={"message": "Hello, World!"}, status_code=200)
