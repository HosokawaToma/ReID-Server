import fastapi
from fastapi import UploadFile, Form, Header
from application.identify_person import ApplicationIdentifyPerson
from application.login import ApplicationLogin
from typing import Annotated
from datetime import datetime
from PIL import Image
import io
from entities.identify_person.image import EntityIdentifyPersonImage

class PresentationIdentifyPerson:
    def __init__(
        self,
        login: ApplicationLogin,
        identify_person: ApplicationIdentifyPerson
        ):
        self.login = login
        self.identify_person = identify_person

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/identify_person", self.endpoint, methods=["POST"])
        app.add_event_handler("shutdown", self.identify_person.shutdown)
        app.add_event_handler("startup", self.identify_person.startup)

    async def endpoint(
        self,
        authorization: Annotated[str, Header()],
        images: list[UploadFile],
        timestamp: str = Form(...),
    ):
        client_id = self.login.authenticate_token(authorization)
        if client_id is None:
            return {"message": "Invalid token"}
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        for image in images:
            image_bytes = await image.read()
            image_pil = Image.open(io.BytesIO(image_bytes))
            if image_pil.mode != "RGB":
                image_pil = image_pil.convert("RGB")
            identify_person_image = EntityIdentifyPersonImage(
                client_id, image_pil, timestamp)
            await self.identify_person.identify_person(identify_person_image)

