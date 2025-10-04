import fastapi

from entities.request.login import EntitiesRequestLogin
from application.login import ApplicationLogin
from application.environment import ApplicationEnvironment


class PresentationLogin:
    def __init__(self):
        self.application_environment = ApplicationEnvironment()
        self.jwt_secret_key = self.application_environment.get_jwt_secret_key()
        self.jwt_algorithm = self.application_environment.get_jwt_algorithm()
        self.application_login = ApplicationLogin(
            self.jwt_secret_key, self.jwt_algorithm)

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/login", self.login, methods=["POST"])

    def login(self, request: EntitiesRequestLogin):
        return self.application_login.login(request.client_id, request.password)
