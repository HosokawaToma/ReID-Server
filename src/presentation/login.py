import fastapi

from entities.request.login import EntitiesRequestLogin
from application.login import ApplicationLogin


class PresentationLogin:
    def __init__(
        self,
        login: ApplicationLogin
        ):
        self.login = login

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/login", self.endpoint, methods=["POST"])

    def endpoint(self, request: EntitiesRequestLogin):
        return self.login.login(request.client_id, request.password)
