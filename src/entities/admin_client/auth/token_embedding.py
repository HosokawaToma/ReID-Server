from dataclasses import dataclass

from errors.entities.admin_client import ErrorEntitiesAdminClientAuthTokenEmbedding

@dataclass
class EntityAdminClientAuthTokenEmbedding:
    TOKEN_PAYLOAD_KEY = "id"

    id: str

    def to_dict(self) -> dict:
        return {
            self.TOKEN_PAYLOAD_KEY: self.id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "EntityAdminClientAuthTokenEmbedding":
        id = data.get(cls.TOKEN_PAYLOAD_KEY)
        if not id or not isinstance(id, str):
            raise ErrorEntitiesAdminClientAuthTokenEmbedding
        return cls(id=id)
