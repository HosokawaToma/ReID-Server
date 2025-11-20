from applications.log import ApplicationLog
from typing import Any
from fastapi import FastAPI

class PresentationBase:
    path: str
    method: list[str]

    def __init__(self, log: ApplicationLog):
        self.log = log

    def setup(self, fastapi_app: FastAPI) -> None:
        fastapi_app.add_api_route(self.path, self.handle, methods=self.method)

    def handle(self) -> Any:
        pass
