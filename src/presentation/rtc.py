import fastapi
from typing import Annotated
from fastapi import Header

from entities.request.rtc import EntitiesRequestRtc
from application.rtc import ApplicationRtc
from application.login import ApplicationLogin
from application.environment import ApplicationEnvironment


class PresentationRtc:
    def __init__(self):
        self.environment = ApplicationEnvironment()
        self.jwt_secret_key = self.environment.get_jwt_secret_key()
        self.jwt_algorithm = self.environment.get_jwt_algorithm()
        self.server_ip = self.environment.get_server_ip()
        self.turn_username = self.environment.get_turn_username()
        self.turn_password = self.environment.get_turn_password()
        self.application_login = ApplicationLogin(
            self.jwt_secret_key, self.jwt_algorithm)
        self.application_rtc = ApplicationRtc(
            self.server_ip, self.turn_username, self.turn_password)

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/rtc/offer", self.offer_endpoint, methods=["POST"])

    async def offer_endpoint(self, authorization: Annotated[str, Header()], request: EntitiesRequestRtc):
        client_id = self.application_login.authenticate_token(authorization)
        if client_id is None:
            return {"message": "Invalid token"}
        return await self.application_rtc.offer(client_id, request.sdp, request.type)
