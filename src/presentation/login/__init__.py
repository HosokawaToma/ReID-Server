import fastapi
from fastapi.responses import JSONResponse
from applications.login import ApplicationLogin
from presentation.login.request import PresentationLoginRequest


class PresentationLogin():
    def __init__(
        self,
        application: ApplicationLogin
        ):
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/login", self.endpoint, methods=["POST"])

    def endpoint(self, request: PresentationLoginRequest):
        try:
            return self.application.login(request.client_id, request.password)
        except Exception as e:
            return JSONResponse(content={"message": str(e)}, status_code=400)
