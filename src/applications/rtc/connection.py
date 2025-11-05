from modules.authenticator.camera_client import ModuleAuthenticatorCameraClient
from entities.rtc.sdp import EntityRtcSdp
from entities.rtc.ice_server import EntityRtcIceServer
from applications.rtc.peer_connection import ApplicationRtcPeerConnection
from entities.storage import EntityStorage
from aiortc import RTCConfiguration, RTCIceServer
from entities.environment.jwt import EntityEnvironmentJwt
from entities.environment.coturn import EntityEnvironmentCoturn
from entities.environment.storage import EntityEnvironmentStorage
from entities.jwt.camera_client import EntityJWTCameraClient
from typing import Dict


class ApplicationRtcConnection:
    def __init__(
        self,
        authenticator: ModuleAuthenticatorCameraClient,
        configuration: RTCConfiguration,
        storage: EntityStorage,
    ):
        self.authenticator = authenticator
        self.configuration = configuration
        self.storage = storage
        self.peer_connections: Dict[str, ApplicationRtcPeerConnection] = {}

    @classmethod
    def create(
        cls,
        environment_jwt: EntityEnvironmentJwt,
        environment_coturn: EntityEnvironmentCoturn,
        environment_storage: EntityEnvironmentStorage,
    ) -> "ApplicationRtcConnection":
        ice_server = EntityRtcIceServer(
            host=environment_coturn.host,
            port=environment_coturn.port,
            username=environment_coturn.username,
            credential=environment_coturn.credential,
        )
        return cls(
            authenticator=ModuleAuthenticatorCameraClient(
                secret_key=environment_jwt.secret_key,
                algorithm=environment_jwt.algorithm,
                expire_days=environment_jwt.expire_days,
            ),
            configuration=RTCConfiguration(
                iceServers=[
                    RTCIceServer(
                        urls=ice_server.urls,
                        credential=ice_server.credential,
                        username=ice_server.username,
                    ),
                ],
            ),
            storage=EntityStorage(path=environment_storage.path),
        )

    def authenticate(self, authorization: str) -> EntityJWTCameraClient:
        return self.authenticator.verify(authorization)

    async def connect(
        self,
        jwt_camera_client: EntityJWTCameraClient,
        offer_sdp: EntityRtcSdp,
    ) -> EntityRtcSdp:
        key = f"{jwt_camera_client.camera_id}:{jwt_camera_client.view_id}"

        async def on_close():
            if key in self.peer_connections:
                del self.peer_connections[key]

        peer_connection = ApplicationRtcPeerConnection(
            jwt_camera_client=jwt_camera_client,
            offer_sdp=offer_sdp,
            configuration=self.configuration,
            storage=self.storage,
            on_close=on_close,
        )
        self.peer_connections[key] = peer_connection
        return await peer_connection.offer()
