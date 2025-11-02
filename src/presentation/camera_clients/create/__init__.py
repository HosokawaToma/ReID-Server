import fastapi
from typing import Annotated
from fastapi import Header
from fastapi.responses import JSONResponse
from applications.camera_clients.create import ApplicationCameraClientsCreate
from presentation.camera_clients.create.request import PresentationCameraClientsCreateRequest
from src.entities.camera_client import EntityCameraClient

class PresentationCameraClientsCreate():
    def __init__(
        self,
        application: ApplicationCameraClientsCreate
    ):
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/camera_clients/create", self.endpoint, methods=["POST"])

    def endpoint(
        self,
        authorization: Annotated[str, Header()],
        request: PresentationCameraClientsCreateRequest
        ):
        try:
            self.application.authenticate(authorization)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=401)
        try:
            self.application.create(
                EntityCameraClient(
                    id=request.camera_client_id,
                    password=request.password,
                    camera_id=request.camera_id,
                    view_id=request.view_id,
                )
            )
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
        finally:
            return JSONResponse(content={"message": "Camera client created"}, status_code=201)
