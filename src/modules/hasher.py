import hashlib
import hmac

class ModuleHasherError(Exception):
    pass

class ModuleHasher:
    def __init__(self, secret: str):
        self.secret = secret

    def hash(self, data: str) -> str:
        return hmac.new(self.secret.encode(), data.encode(), hashlib.sha256).hexdigest()

    def matches(self, data: str, hash: str) -> None:
        if not hmac.compare_digest(self.hash(data), hash):
            raise ModuleHasherError
