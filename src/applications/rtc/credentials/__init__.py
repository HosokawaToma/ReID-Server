from entities.camera_client import EntityCameraClient
from modules.authenticator.camera_client import ModuleAuthenticatorCameraClient
from applications.rtc.credentials.ice_servers import ApplicationRtcCredentialsIceServers
from entities.environment.jwt import EntityEnvironmentJwt
from entities.environment.coturn import EntityEnvironmentCoturn

class ApplicationRtcCredentials:
    def __init__(self, authenticator: ModuleAuthenticatorCameraClient, ice_servers: ApplicationRtcCredentialsIceServers):
        self.authenticator = authenticator
        self.ice_servers = ice_servers

    @classmethod
    def create(cls, environment_jwt: EntityEnvironmentJwt, environment_coturn: EntityEnvironmentCoturn):
        return cls(
            authenticator=ModuleAuthenticatorCameraClient(
                jwt_secret_key=environment_jwt.secret_key,
                jwt_algorithm=environment_jwt.algorithm,
                expire_days=environment_jwt.expire_days,
            ),
            ice_servers=ApplicationRtcCredentialsIceServers(
                environment=environment_coturn,
            ),
        )

    def authenticate(self, authorization: str) -> EntityCameraClient:
        return self.authenticator.verify(authorization)

    def generate_turn_ice_servers(self, client_id: str) -> dict:
        return self.ice_servers.generate(client_id)
