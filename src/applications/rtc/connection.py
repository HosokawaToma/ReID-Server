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
from typing import List


class ApplicationRtcConnection:
    def __init__(
        self,
        configuration: RTCConfiguration,
        storage: EntityStorage,
    ):
        self.configuration = configuration
        self.storage = storage
        self.peer_connections: List[ApplicationRtcPeerConnection] = []

    @classmethod
    def create(
        cls,
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

    async def connect(
        self,
        jwt_camera_client: EntityJWTCameraClient,
        offer_sdp: EntityRtcSdp,
    ) -> EntityRtcSdp:
        peer_connection = ApplicationRtcPeerConnection(
            jwt_camera_client=jwt_camera_client,
            offer_sdp=offer_sdp,
            configuration=self.configuration,
            storage=self.storage,
        )
        self.peer_connections.append(peer_connection)
        return await peer_connection.offer()
