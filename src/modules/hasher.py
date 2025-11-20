import hashlib
import hmac

from errors.modules.hasher import ErrorModuleHasherInvalidCredential

class ModuleHasher:
    def hash(self, value: str) -> str:
        return hashlib.sha256(value.encode()).hexdigest()

    def assert_valid(self, value: str, hashed_value: str) -> None:
        if not hmac.compare_digest(self.hash(value), hashed_value):
            raise ErrorModuleHasherInvalidCredential
