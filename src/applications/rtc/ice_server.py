from entities.rtc.ice_server import EntityRtcIceServer
from entities.environment.coturn import EntityEnvironmentCoturn
from modules.authenticator.camera_client import ModuleAuthenticatorCameraClient
from entities.environment.jwt import EntityEnvironmentJwt
from entities.camera_client import EntityCameraClient

class ApplicationRtcIceServer:
    def __init__(self, host: str, port: str, username: str, password: str, authenticator: ModuleAuthenticatorCameraClient):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.authenticator = authenticator

    @classmethod
    def create(cls, environment_coturn: EntityEnvironmentCoturn, environment_jwt: EntityEnvironmentJwt) -> "ApplicationRtcIceServer":
        return cls(
            host=environment_coturn.host,
            port=environment_coturn.secure_port,
            username=environment_coturn.username,
            password=environment_coturn.password,
            authenticator=ModuleAuthenticatorCameraClient(
                secret_key=environment_jwt.secret_key,
                algorithm=environment_jwt.algorithm,
                expire_days=environment_jwt.expire_days,
            ),
        )

    def authenticate(self, authorization: str) -> EntityCameraClient:
        return self.authenticator.verify(authorization)

    def generate(self) -> EntityRtcIceServer:
        return EntityRtcIceServer(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
        )
