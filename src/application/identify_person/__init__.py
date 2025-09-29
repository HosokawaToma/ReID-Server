from typing import Union
from fastapi import FastAPI, Form, Header, HTTPException, UploadFile

from application.identify_person.background_process import ApplicationIdentifyPersonBackgroundProcess
from application.identify_person.response_parser import ApplicationIdentifyPersonResponseParser
from service.authentication import ServiceAuthentication

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
        x_header: Union[str, None] = Header(default=None),
    ) -> None:
        if x_header is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        x_header_value = x_header.split(" ")
        if len(x_header_value) != 2:
            raise HTTPException(status_code=401, detail="Unauthorized")
        if x_header_value[0] != "Bearer":
            raise HTTPException(status_code=401, detail="Unauthorized")
        x_header_token = x_header_value[1]
        client_jwt_token = ServiceAuthentication.verify_jwt_token_for_client(x_header_token)
        if client_jwt_token is None:
            raise HTTPException(status_code=401, detail="Unauthorized")

        person_crop_images = await ApplicationIdentifyPersonResponseParser.parse(
            images,
            camera_id,
            view_id,
            timestamp
        )
        for person_crop_image in person_crop_images:
            await ApplicationIdentifyPersonBackgroundProcess.add_task(person_crop_image)
