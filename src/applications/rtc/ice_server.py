from entities.rtc.ice_server import EntityRtcIceServer
from entities.environment.coturn import EntityEnvironmentCoturn
from modules.authenticator.camera_client import ModuleAuthenticatorCameraClient
from entities.environment.jwt import EntityEnvironmentJwt
from entities.jwt.camera_client import EntityJWTCameraClient

import time
import base64
import hmac
import hashlib


class ApplicationRtcIceServer:
    def __init__(self, host: str, port: str, secret: str, ttl: int, authenticator: ModuleAuthenticatorCameraClient):
        self.host = host
        self.port = port
        self.secret = secret
        self.ttl = ttl
        self.authenticator = authenticator

    @classmethod
    def create(cls, environment_coturn: EntityEnvironmentCoturn, environment_jwt: EntityEnvironmentJwt) -> "ApplicationRtcIceServer":
        return cls(
            host=environment_coturn.host,
            port=environment_coturn.secure_port,
            secret=environment_coturn.secret,
            ttl=environment_coturn.ttl,
            authenticator=ModuleAuthenticatorCameraClient(
                secret_key=environment_jwt.secret_key,
                algorithm=environment_jwt.algorithm,
                expire_days=environment_jwt.expire_days,
            ),
        )

    def authenticate(self, authorization: str) -> EntityJWTCameraClient:
        return self.authenticator.verify(authorization)

    def generate(self, camera_client_id: str) -> EntityRtcIceServer:
        username, password = self._generate_turn_credentials(camera_client_id)
        return EntityRtcIceServer(
            host=self.host,
            port=self.port,
            username=username,
            password=password,
        )

    def _generate_turn_credentials(self, camera_client_id: str) -> tuple[str, str]:
        timestamp = int(time.time()) + self.ttl
        username = f"{timestamp}:{camera_client_id}"

        # HMAC-SHA1でパスワードを生成
        mac = hmac.new(
            self.secret.encode('utf-8'),
            username.encode('utf-8'),
            hashlib.sha1
        )
        password = base64.b64encode(mac.digest()).decode('utf-8')

        return username, password
