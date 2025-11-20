from entities.environment.token_policy import EntityEnvironmentTokenPolicy
from entities.camera_client.auth.token import EntityCameraClientAuthToken
import jwt
from errors.modules.token import ErrorModuleTokenVerifier

class ModuleTokenVerifier:
    def __init__(self, environment: EntityEnvironmentTokenPolicy) -> None:
        self.environment = environment

    def verify(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.environment.secret_key, algorithms=[self.environment.algorithm])
        except jwt.ExpiredSignatureError:
            raise ErrorModuleTokenVerifier("Token expired")
        except jwt.InvalidTokenError:
            raise ErrorModuleTokenVerifier("Invalid token")
