import fastapi
from applications.auth.admin_client import ApplicationAuthAdminClient
from applications.identify_person.refresh import ApplicationIdentifyPersonRefresh
from typing import Annotated
from fastapi import Header
from fastapi.responses import JSONResponse
from presentation.identify_person.refresh.request import PresentationIdentifyPersonRefreshRequest
from presentation.background.person.feature.create import PresentationBackgroundPersonFeatureCreateQueue
from presentation.background.person.feature.create import PresentationBackgroundPersonFeatureCreateQueueItem
from presentation.background.person.feature.identify import PresentationBackgroundPersonFeatureIdentifyQueue
from presentation.background.person.feature.identify import PresentationBackgroundPersonFeatureIdentifyQueueItem

class PresentationIdentifyPersonRefresh:
    def __init__(
        self,
        application_auth: ApplicationAuthAdminClient,
        application: ApplicationIdentifyPersonRefresh,
        person_feature_create_queue: PresentationBackgroundPersonFeatureCreateQueue,
        person_feature_identify_queue: PresentationBackgroundPersonFeatureIdentifyQueue,
        ):
        self.application_auth = application_auth
        self.application = application
        self.person_feature_create_queue = person_feature_create_queue
        self.person_feature_identify_queue = person_feature_identify_queue

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
                self.person_feature_create_queue.put(
                    PresentationBackgroundPersonFeatureCreateQueueItem(
                        person_image_path.image_id,
                        callback=lambda person_feature_id: self.person_feature_identify_queue.put(
                            PresentationBackgroundPersonFeatureIdentifyQueueItem(
                                person_feature_id,
                            )
                        ),
                    )
                )
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
        return JSONResponse(content={"message": "Identify person refreshed successfully"}, status_code=200)
