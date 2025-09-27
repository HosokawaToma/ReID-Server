from fastapi import FastAPI
from application.login import ApplicationLogin


class PresentationLogin:
    @staticmethod
    def setup(fastapi_app: FastAPI):
        fastapi_app.add_api_route(
            "/login", PresentationLogin.endpoint, methods=["POST"])

    @staticmethod
    def endpoint(client_id: str, password: str):
        return ApplicationLogin.process(client_id, password)
