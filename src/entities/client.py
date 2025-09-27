import hashlib

class Client:
    def __init__(self, id: str, password: str):
        self.id = id
        self.password = password
        self.hashed_password = self.hash_password(password)

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
