import fastapi
from fastapi.responses import JSONResponse
from applications.login.client import ApplicationLoginClient
from presentation.login.client.request import PresentationLoginClientRequest


class PresentationLoginClient():
    def __init__(
        self,
        application: ApplicationLoginClient
    ):
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/login/client",
                          self.endpoint, methods=["POST"])

    def endpoint(self, request: PresentationLoginClientRequest):
        try:
            return self.application.login(request.client_id, request.password)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
