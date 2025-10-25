import fastapi
from typing import Annotated
from fastapi import Header

from entities.request.rtc import EntitiesRequestRtc
from application.rtc import ApplicationRtc
from application.login import ApplicationLogin


class PresentationRtc:
    def __init__(
        self,
        rtc: ApplicationRtc,
        login: ApplicationLogin
        ):
        self.rtc = rtc
        self.login = login

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/rtc/offer", self.endpoint_offer, methods=["POST"])

    async def endpoint_offer(self, authorization: Annotated[str, Header()], request: EntitiesRequestRtc):
        client_id = self.login.authenticate_token(authorization)
        if client_id is None:
            return {"message": "Invalid token"}
        return await self.rtc.offer(client_id, request.sdp, request.type)
