import fastapi
from fastapi.responses import JSONResponse
from applications.auth.login.admin_client import ApplicationAuthLoginAdminClient
from presentation.auth.login.admin_client.request import PresentationAuthLoginAdminClientRequest


class PresentationAuthLoginAdminClient():
    def __init__(
        self,
        application: ApplicationAuthLoginAdminClient
    ):
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/auth/login/admin_client",
                          self.endpoint, methods=["POST"])

    def endpoint(self, request: PresentationAuthLoginAdminClientRequest):
        try:
            return self.application.login(request.admin_client_id, request.password)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
