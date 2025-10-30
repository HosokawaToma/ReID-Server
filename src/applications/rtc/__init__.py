from applications.rtc.peer_connection import ApplicationRtcPeerConnection
from applications.rtc.configuration import ApplicationRtcConfiguration
from modules.authenticator import ModuleAuthenticator
from entities.client import EntityClient


class ApplicationRtc:
    def __init__(
        self,
        configuration: ApplicationRtcConfiguration,
        authenticator: ModuleAuthenticator
        ):
        self.peer_connections: list[ApplicationRtcPeerConnection] = []
        self.configuration = configuration
        self.authenticator = authenticator

    @classmethod
    def create(
        cls,
        jwt_secret_key: str,
        jwt_algorithm: str,
        host: str,
        port: str,
        username: str,
        password: str,
        ) -> "ApplicationRtc":
        return cls(
            configuration=ApplicationRtcConfiguration(host=host, port=port, username=username, password=password),
            authenticator=ModuleAuthenticator(jwt_secret_key=jwt_secret_key, jwt_algorithm=jwt_algorithm)
        )

    def authenticate(self, authorization: str) -> EntityClient:
        return self.authenticator.authenticate(authorization)

    async def offer(self, client_id: int, sdp: str, sdp_type: str):
        peer_connection = ApplicationRtcPeerConnection(client_id, self.configuration)
        self.peer_connections.append(peer_connection)
        return await peer_connection.offer(sdp, sdp_type)
