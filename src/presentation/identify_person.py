import fastapi
from typing import Annotated
from fastapi import UploadFile, Form, Header
from applications.identify_person import ApplicationIdentifyPerson
from entities.image import EntityImage
from fastapi.responses import JSONResponse
from applications.auth.camera_client import ApplicationAuthCameraClient

class PresentationIdentifyPerson:
    def __init__(
        self,
        application_auth: ApplicationAuthCameraClient,
        application: ApplicationIdentifyPerson
        ):
        self.application_auth = application_auth
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/identify_person", self.endpoint, methods=["POST"])
        app.add_event_handler("startup", self.application.start)
        app.add_event_handler("shutdown", self.application.stop)

    async def endpoint(
        self,
        authorization: Annotated[str, Header()],
        images: list[UploadFile],
        timestamp: str = Form(...),
    ):
        try:
            token = self.application_auth.parse(authorization)
            camera_client = self.application_auth.verify(token)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=401)
        try:
            timestamp_datetime = self.application.from_iso_format(timestamp)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
        for image in images:
            try:
                image = self.application.decode_image(await image.read())
            except Exception as e:
                return JSONResponse(content={"message": str(e)}, status_code=400)
            try:
                await self.application.identify(
                    EntityImage(
                        id=None,
                        image=image,
                        camera_id=camera_client.camera_id,
                        view_id=camera_client.view_id,
                        timestamp=timestamp_datetime,
                    )
                )
            except Exception as e:
                return JSONResponse(content={"message": str(e)}, status_code=400)
        return JSONResponse(content={"message": "Person identified successfully"}, status_code=200)
