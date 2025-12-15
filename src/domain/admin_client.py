from dataclasses import dataclass
from domain.token_converter import DomainTokenConverter
import time

@dataclass
class DomainAdminClient:
    id: str
    password: str

    def authenticate(self, id: str, password: str) -> bool:
        return self.id == id and self.password == password

    def generate_token(self, token_converter: DomainTokenConverter) -> str:
        payload = {
            "id": self.id,
            "expire_time": int(time.time() + token_converter.expire_minutes * 60)
        }
        return token_converter.encode(payload)

    def verify_token(self, token: str, token_converter: DomainTokenConverter) -> str | None:
        payload = token_converter.decode(token)
        if not isinstance(payload, dict):
            return None
        if "id" not in payload:
            return None
        if "expire_time" not in payload:
            return None
        if not isinstance(payload["id"], str):
            return None
        if not isinstance(payload["expire_time"], int):
            return None
        if payload["id"] != self.id:
            return None
        if payload["expire_time"] < time.time():
            return None
        return payload["id"]
