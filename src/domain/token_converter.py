import jwt
from dataclasses import dataclass

class DomainTokenConverterError(Exception):
    pass

@dataclass
class DomainTokenConverter:
    secret_key: str
    algorithm: str
    expire_minutes: int

    def encode(self, payload: dict) -> str:
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.InvalidTokenError:
            raise DomainTokenConverterError("Invalid token")
