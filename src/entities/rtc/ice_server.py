from dataclasses import dataclass, field, InitVar

@dataclass
class EntityRtcIceServer:
    host: InitVar[str]
    port: InitVar[str]
    username: str
    password: str
    urls: list[str] = field(init=False)

    def __post_init__(self):
        self.urls = [f"stun:{self.host}:{self.port}", f"turn:{self.host}:{self.port}"]

    def to_dict(self) -> dict:
        return {
            "urls": self.urls,
            "username": self.username,
            "password": self.password,
        }
