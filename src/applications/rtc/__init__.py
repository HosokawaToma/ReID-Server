from applications.rtc.peer_connection import ApplicationRtcPeerConnection
from applications.rtc.configuration import ApplicationRtcConfiguration
from modules.authenticator.camera_client import ModuleAuthenticatorCameraClient
from entities.camera_client import EntityCameraClient
from entities.environment.jwt import EntityEnvironmentJwt
from entities.environment.coturn import EntityEnvironmentCoturn


class ApplicationRtc:
    def __init__(
        self,
        configuration: ApplicationRtcConfiguration,
        authenticator: ModuleAuthenticatorCameraClient
        ):
        self.peer_connections: list[ApplicationRtcPeerConnection] = []
        self.configuration = configuration
        self.authenticator = authenticator

    @classmethod
    def create(
        cls,
        environment_jwt: EntityEnvironmentJwt,
        environment_coturn: EntityEnvironmentCoturn,
        ) -> "ApplicationRtc":
        return cls(
            configuration=ApplicationRtcConfiguration(
                host=environment_coturn.host,
                port=environment_coturn.secure_port,
                username=environment_coturn.username,
                password=environment_coturn.password,
            ),
            authenticator=ModuleAuthenticatorCameraClient(
                jwt_secret_key=environment_jwt.secret_key,
                jwt_algorithm=environment_jwt.algorithm,
            ),
        )

    def authenticate(self, authorization: str) -> EntityCameraClient:
        return self.authenticator.authenticate(authorization)

    async def offer(self, client_id: int, sdp: str, sdp_type: str):
        peer_connection = ApplicationRtcPeerConnection(client_id, self.configuration)
        self.peer_connections.append(peer_connection)
        return await peer_connection.offer(sdp, sdp_type)
