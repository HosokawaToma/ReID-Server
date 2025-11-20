import jwt
from entities.environment.token_policy import EntityEnvironmentTokenPolicy
import time
from errors.modules.token import ErrorModuleTokenGenerator

class ModuleTokenGenerator:
    EXPIRE_TIME_KEY = "exp"

    def __init__(self, environment: EntityEnvironmentTokenPolicy) -> None:
        self.environment = environment

    def generate(self, payload: dict) -> str:
        try:
            return jwt.encode(
                {
                    **payload,
                    self.EXPIRE_TIME_KEY: int(time.time()) + self.environment.expire_minutes * 60,
                },
                self.environment.secret_key,
                algorithm=self.environment.algorithm,
            )
        except Exception as e:
            raise ErrorModuleTokenGenerator(f"Failed to generate token: {e}")
