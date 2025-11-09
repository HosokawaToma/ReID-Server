import fastapi
from typing import Annotated
from fastapi import Header
from fastapi.responses import JSONResponse
from applications.camera_clients.create import ApplicationCameraClientsCreate
from presentation.camera_clients.create.request import PresentationCameraClientsCreateRequest
from entities.camera_client import EntityCameraClient
from applications.auth.admin_client import ApplicationAuthAdminClient

class PresentationCameraClientsCreate():
    def __init__(
        self,
        application_auth: ApplicationAuthAdminClient,
        application: ApplicationCameraClientsCreate
    ):
        self.application_auth = application_auth
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/camera_clients/create", self.endpoint, methods=["POST"])

    def endpoint(
        self,
        authorization: Annotated[str, Header()],
        request: PresentationCameraClientsCreateRequest
        ):
        try:
            _, token = self.application_auth.parse(authorization)
            self.application_auth.verify(token)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=401)
        try:
            self.application.create_camera_client(
                EntityCameraClient(
                    id=request.camera_client_id,
                    password=request.password,
                    hashed_password=None,
                    camera_id=request.camera_id,
                    view_id=request.view_id,
                )
            )
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
        finally:
            return JSONResponse(content={"message": "Camera client created"}, status_code=201)
