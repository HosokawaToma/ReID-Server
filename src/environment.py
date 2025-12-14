import os
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class EnvironmentHash:
    secret: str
@dataclass
class Environment:
    app_host: str = field(init=False)
    app_port: int = field(init=False)
    hash_key: str = field(init=False)
    public_ip: str = field(init=False)
    admin_client_id: str = field(init=False)
    admin_client_password: str = field(init=False)
    jwt_secret_key: str = field(init=False)
    jwt_algorithm: str = field(init=False)
    jwt_expire_minutes: int = field(init=False)
    jwt_refresh_secret_key: str = field(init=False)
    jwt_refresh_algorithm: str = field(init=False)
    jwt_refresh_expire_minutes: int = field(init=False)
    database_host: str = field(init=False)
    database_port: str = field(init=False)
    database_database: str = field(init=False)
    database_user: str = field(init=False)
    database_password: str = field(init=False)
    storage_directory: Path = field(init=False)
    redis_host: str = field(init=False)
    redis_port: int = field(init=False)
    redis_db: int = field(init=False)
    coturn_host: str = field(init=False)
    coturn_port: str = field(init=False)
    coturn_secret: str = field(init=False)
    coturn_ttl: int = field(init=False)
    coturn_username: str = field(init=False)
    coturn_credential: str = field(init=False)

    def __post_init__(self):
        self.app_host = self._get_string("APP_HOST")
        self.app_port = self._get_int("APP_PORT")
        self.hash_key = self._get_string("HASH_KEY")
        self.public_ip = self._get_string("PUBLIC_IP")
        self.admin_client_id = self._get_string("ADMIN_CLIENT_ID")
        self.admin_client_password = self._get_string("ADMIN_CLIENT_PASSWORD")
        self.jwt_secret_key = self._get_string("JWT_SECRET_KEY")
        self.jwt_algorithm = self._get_string("JWT_ALGORITHM")
        self.jwt_expire_minutes = self._get_int("JWT_EXPIRE_MINUTES")
        self.jwt_refresh_secret_key = self._get_string("JWT_REFRESH_SECRET_KEY")
        self.jwt_refresh_algorithm = self._get_string("JWT_REFRESH_ALGORITHM")
        self.jwt_refresh_expire_minutes = self._get_int("JWT_REFRESH_EXPIRE_MINUTES")
        self.database_host = self._get_string("POSTGRESQL_HOST")
        self.database_port = self._get_string("POSTGRESQL_PORT")
        self.database_database = self._get_string("POSTGRESQL_DATABASE")
        self.database_user = self._get_string("POSTGRESQL_USER")
        self.database_password = self._get_string("POSTGRESQL_PASSWORD")
        self.storage_directory = Path(self._get_string("STORAGE_PATH"))
        self.redis_host = self._get_string("REDIS_HOST")
        self.redis_port = self._get_int("REDIS_PORT")
        self.redis_db = self._get_int("REDIS_DB")
        self.coturn_host = self._get_string("COTURN_HOST")
        self.coturn_port = self._get_string("COTURN_PORT")
        self.coturn_secret = self._get_string("COTURN_SECRET")
        self.coturn_ttl = self._get_int("COTURN_TTL")
        self.coturn_username = self._get_string("COTURN_USERNAME")
        self.coturn_credential = self._get_string("COTURN_CREDENTIAL")

    def _get_string(self, key: str) -> str:
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"{key} is not set")
        return value

    def _get_int(self, key: str) -> int:
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"{key} is not set")
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"{key} is not a valid integer")
