import time
import hmac
import hashlib
import base64

from entities.environment.coturn import EntityEnvironmentCoturn

class ApplicationRtcCredentialsIceServers:
    def __init__(self, environment: EntityEnvironmentCoturn):
        self.environment = environment

    def generate(self, client_id: str) -> dict:
        exp = int(time.time()) + self.environment.ttl
        username = f"{exp}:{client_id}"
        credential = base64.b64encode(hmac.new(
            self.environment.secret.encode(),
            username.encode(),
            hashlib.sha1
        ).digest()).decode()
        return {
            "iceServers": [
                {
                    "urls": [
                        f"stun:{self.environment.host}:{self.environment.secure_port}",
                        f"turn:{self.environment.host}:{self.environment.secure_port}",
                    ],
                    "username": username,
                    "credential": credential,
                    "ttl": self.environment.ttl,
                }
            ]
        }

