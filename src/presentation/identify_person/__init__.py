import fastapi
from typing import Annotated
from fastapi import Header, UploadFile
from applications.identify_person import ApplicationIdentifyPerson
from fastapi.responses import JSONResponse
from applications.auth.camera_client import ApplicationAuthCameraClient
from presentation.background.person.feature.create import PresentationBackgroundPersonFeatureCreateQueue
from presentation.background.person.feature.create import PresentationBackgroundPersonFeatureCreateQueueItem
from presentation.background.person.feature.identify import PresentationBackgroundPersonFeatureIdentifyQueue
from presentation.background.person.feature.identify import PresentationBackgroundPersonFeatureIdentifyQueueItem
class PresentationIdentifyPerson:
    def __init__(
        self,
        application_auth: ApplicationAuthCameraClient,
        application: ApplicationIdentifyPerson,
        person_feature_create_queue: PresentationBackgroundPersonFeatureCreateQueue,
        person_feature_identify_queue: PresentationBackgroundPersonFeatureIdentifyQueue,
        ):
        self.application_auth = application_auth
        self.application = application
        self.person_feature_create_queue = person_feature_create_queue
        self.person_feature_identify_queue = person_feature_identify_queue

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/identify_person", self.endpoint, methods=["POST"])

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
                self.person_feature_create_queue.put(
                    PresentationBackgroundPersonFeatureCreateQueueItem(
                        person_image.id,
                        callback=lambda person_feature_id: self.person_feature_identify_queue.put(
                            PresentationBackgroundPersonFeatureIdentifyQueueItem(
                                person_feature_id,
                            )
                        ),
                    )
                )
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
        return JSONResponse(content={"message": "Person images saved successfully. Person identification will be processed in background."}, status_code=200)
