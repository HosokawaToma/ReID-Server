import fastapi
from fastapi.responses import JSONResponse
from applications.auth.admin_client import ApplicationAuthAdminClient
from applications.identify_person.search import ApplicationIdentifyPersonSearch
from typing import Annotated
from fastapi import Header
from .request import PresentationIdentifyPersonSearchRequest
from entities.application.identify_person.search.conditions import EntityApplicationIdentifyPersonSearchConditions

class PresentationIdentifyPersonSearch:
    def __init__(self, application_auth: ApplicationAuthAdminClient, application: ApplicationIdentifyPersonSearch):
        self.application_auth = application_auth
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/identify_person/search", self.endpoint, methods=["POST"])

    async def endpoint(self, authorization: Annotated[str, Header()], request: PresentationIdentifyPersonSearchRequest):
        try:
            token = self.application_auth.parse(authorization)
            camera_client = self.application_auth.verify(token)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=401)
        try:
            return_values = self.application.search(EntityApplicationIdentifyPersonSearchConditions(
                after=request.after,
                before=request.before,
                view_ids=request.view_ids,
                camera_ids=request.camera_ids,
                image_ids=request.image_ids,
                person_ids=request.person_ids,
            ))
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=500)
        return JSONResponse(content=[return_value.to_dict() for return_value in return_values], status_code=200)
