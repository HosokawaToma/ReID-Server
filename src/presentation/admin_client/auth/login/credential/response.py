from dataclasses import dataclass
from starlette.responses import Response

@dataclass
class PresentationAdminClientAuthLoginCredentialResponse(Response):
    message: str

    def __post_init__(self):
        self.status_code = 200
        self.content = {"message": self.message}
        self.headers = {"Content-Type": "application/json"}
