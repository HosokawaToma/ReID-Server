import fastapi
from typing import Annotated
from fastapi import Form, Header, UploadFile
from applications.identify_person import ApplicationIdentifyPerson
from fastapi.responses import JSONResponse
from applications.auth.camera_client import ApplicationAuthCameraClient
from applications.identify_person.background.feature import ApplicationIdentifyPersonBackgroundFeature
from applications.identify_person.background.identify import ApplicationIdentifyPersonBackgroundIdentify
from datetime import datetime
import asyncio
class PresentationIdentifyPerson:
    def __init__(
        self,
        application_auth: ApplicationAuthCameraClient,
        application: ApplicationIdentifyPerson,
        application_background_feature: ApplicationIdentifyPersonBackgroundFeature,
        application_background_identify: ApplicationIdentifyPersonBackgroundIdentify,
        ):
        self.application_auth = application_auth
        self.application = application
        self.application_background_feature = application_background_feature
        self.application_background_identify = application_background_identify

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/identify_person", self.endpoint, methods=["POST"])
        app.add_event_handler("startup", self.application_background_feature.start)
        app.add_event_handler("shutdown", self.application_background_feature.stop)
        app.add_event_handler("startup", self.application_background_identify.start)
        app.add_event_handler("shutdown", self.application_background_identify.stop)

    async def endpoint(
        self,
        authorization: Annotated[str, Header()],
        images: list[UploadFile]
    ):
        try:
            token = self.application_auth.parse(authorization)
            camera_client = self.application_auth.verify(token)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=401)
        try:
            person_images = await self.application.proses(camera_client.id, [await image.read() for image in images])
            for person_image in person_images:
                await self.application_background_feature.queue.add(person_image.id, self.application_background_identify.queue.add)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
        return JSONResponse(content={"message": "Person images saved successfully. Person identification will be processed in background."}, status_code=200)
