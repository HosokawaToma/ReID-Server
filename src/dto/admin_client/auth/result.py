from dataclasses import dataclass

@dataclass
class DtoAdminClientAuthResult:
    token: str
    refresh_token: str
