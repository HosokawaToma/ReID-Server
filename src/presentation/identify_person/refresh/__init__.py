import fastapi
from applications.auth.admin_client import ApplicationAuthAdminClient
from applications.identify_person.refresh import ApplicationIdentifyPersonRefresh
from typing import Annotated
from fastapi import Header
from fastapi.responses import JSONResponse
from presentation.identify_person.refresh.request import PresentationIdentifyPersonRefreshRequest
from applications.identify_person.background.identify.queue import ApplicationIdentifyPersonBackgroundIdentifyQueue
from applications.identify_person.background.feature.queue import ApplicationIdentifyPersonBackgroundFeatureQueue

class PresentationIdentifyPersonRefresh:
    def __init__(
        self,
        application_auth: ApplicationAuthAdminClient,
        application: ApplicationIdentifyPersonRefresh,
        application_background_feature_queue: ApplicationIdentifyPersonBackgroundFeatureQueue,
        application_background_identify_queue: ApplicationIdentifyPersonBackgroundIdentifyQueue,
        ):
        self.application_auth = application_auth
        self.application = application
        self.application_background_identify_queue = application_background_identify_queue
        self.application_background_feature_queue = application_background_feature_queue

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/identify_person/refresh", self.endpoint, methods=["POST"])

    async def endpoint(
        self,
        authorization: Annotated[str, Header()],
        request: PresentationIdentifyPersonRefreshRequest,
    ):
        try:
            token = self.application_auth.parse(authorization)
            self.application_auth.verify(token)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=401)
        try:
            person_image_paths = self.application.refresh_person_image_paths(
                after_timestamp=request.after_timestamp,
                before_timestamp=request.before_timestamp,
                camera_ids=request.camera_ids,
                view_ids=request.view_ids,
            )
            for person_image_path in person_image_paths:
                await self.application_background_feature_queue.add(person_image_path.image_id, self.application_background_identify_queue.add)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
        return JSONResponse(content={"message": "Identify person refreshed successfully"}, status_code=200)
