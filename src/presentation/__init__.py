import fastapi
from application import Application

class Presentation:
    def __init__(
        self,
        application: Application
        ):
        self.application = application

    def setup(self, app: fastapi.FastAPI):
        self.application.startup()
        app.add_event_handler("shutdown", self.application.shutdown)
        app.add_event_handler("startup", self.application.startup)
