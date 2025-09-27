from fastapi import FastAPI, Form, UploadFile

from application.identify_person.background_process import ApplicationIdentifyPersonBackgroundProcess
from application.identify_person.response_parser import ApplicationIdentifyPersonResponseParser

class ApplicationIdentifyPerson:
    @staticmethod
    def setup(fastapi_app: FastAPI):
        fastapi_app.add_api_route(
            "/identify_person", ApplicationIdentifyPerson.endpoint, methods=["POST"])

    @staticmethod
    async def endpoint(
        images: list[UploadFile],
        camera_id: int = Form(...),
        view_id: int = Form(...),
        timestamp: str = Form(...),
    ) -> None:
        person_crop_images = await ApplicationIdentifyPersonResponseParser.parse(
            images,
            camera_id,
            view_id,
            timestamp
        )
        for person_crop_image in person_crop_images:
            await ApplicationIdentifyPersonBackgroundProcess.add_task(person_crop_image)
