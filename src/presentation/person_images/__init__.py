from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse
from typing import Annotated
from fastapi import Header
import uuid
from applications.auth.admin_client import ApplicationAuthAdminClient
from applications.person_images import ApplicationPersonImages


class PresentationPersonImages:
    def __init__(self, application_auth: ApplicationAuthAdminClient, application: ApplicationPersonImages):
        self.application_auth = application_auth
        self.application = application

    def setup(self, app: FastAPI):
        app.add_api_route("/person_images/{image_id}", self.endpoint, methods=["GET"])


    async def endpoint(self, authorization: Annotated[str, Header()], image_id: uuid.UUID):
        try:
            token = self.application_auth.parse(authorization)
            camera_client = self.application_auth.verify(token)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=401)
        try:
            img_buffer = self.application.search(image_id)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=500)
        return StreamingResponse(content=img_buffer, media_type="image/jpeg", status_code=200)
