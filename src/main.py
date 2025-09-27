import fastapi
import uvicorn

from application.identify_person import ApplicationIdentifyPerson
from application.login import ApplicationLogin


class ServerApp:
    def __init__(self):
        self.fastapi_app = fastapi.FastAPI()
        ApplicationIdentifyPerson.setup(self.fastapi_app)
        ApplicationLogin.setup(self.fastapi_app)

    def run(self):
        uvicorn.run(self.fastapi_app, host="0.0.0.0", port=8888)


if __name__ == "__main__":
    app = ServerApp()
    app.run()
