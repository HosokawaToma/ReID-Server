import fastapi
from fastapi.responses import JSONResponse
from applications.login.admin_client import ApplicationLoginAdminClient
from presentation.login.admin_client.request import PresentationLoginAdminClientRequest


class PresentationLoginAdminClient():
    def __init__(
        self,
        application: ApplicationLoginAdminClient
    ):
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/login/admin_client",
                          self.endpoint, methods=["POST"])

    def endpoint(self, request: PresentationLoginAdminClientRequest):
        try:
            return self.application.login(request.admin_client_id, request.password)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
