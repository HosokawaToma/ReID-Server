import fastapi
from typing import Annotated
from fastapi import UploadFile, Form, Header
from applications.identify_person import ApplicationIdentifyPerson
from entities.image import EntityImage
from fastapi.responses import JSONResponse

class PresentationIdentifyPerson:
    def __init__(
        self,
        application: ApplicationIdentifyPerson
        ):
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/identify_person", self.endpoint, methods=["POST"])

    async def endpoint(
        self,
        authorization: Annotated[str, Header()],
        images: list[UploadFile],
        timestamp: str = Form(...),
    ):
        try:
            camera_client = self.application.authenticate(authorization)
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
                self.application.identify(EntityImage(image, camera_client.camera_id, camera_client.view_id, timestamp_datetime))
            except Exception as e:
                return JSONResponse(content={"message": str(e)}, status_code=400)
        return JSONResponse(content={"message": "Person identified successfully"}, status_code=200)
