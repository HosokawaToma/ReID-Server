from modules.authenticator.camera_client import ModuleAuthenticatorCameraClient
from entities.rtc.sdp import EntityRtcSdp
from entities.rtc.ice_server import EntityRtcIceServer
from applications.rtc.peer_connection import ApplicationRtcPeerConnection
from entities.storage import EntityStorage
from aiortc import RTCConfiguration, RTCIceServer
from entities.jwt.camera_client import EntityJWTCameraClient
from typing import List
from environment import Environment

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
        environment: Environment,
    ) -> "ApplicationRtcConnection":
        ice_server = EntityRtcIceServer(
            host=environment.coturn_host,
            port=environment.coturn_port,
            username=environment.coturn_username,
            credential=environment.coturn_credential,
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
            storage=EntityStorage(path=str(environment.storage_directory)),
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
