from dataclasses import dataclass, field, InitVar

@dataclass
class EntityRtcIceServer:
    host: InitVar[str]
    port: InitVar[str]
    username: str
    credential: str
    urls: list[str] = field(init=False)

    def __post_init__(self, host: str, port: str):
        self.urls = [
            f"stun:{host}:{port}",
            f"turn:{host}:{port}",
        ]

    def to_dict(self) -> dict:
        return {
            "urls": self.urls,
            "username": self.username,
            "credential": self.credential,
        }
