import os

class Environment:

    def host(self) -> str:
        value = os.getenv("HOST")
        if value is None:
            raise ValueError("HOST is not set")
        return value

    def port(self) -> int:
        value = os.getenv("PORT")
        if value is None:
            raise ValueError("PORT is not set")
        try:
            return int(value)
        except ValueError:
            raise ValueError("PORT is not a valid integer")

    def public_ip(self) -> str:
        value = os.getenv("PUBLIC_IP")
        if value is None:
            raise ValueError("PUBLIC_IP is not set")
        return value

    def jwt_secret_key(self) -> str:
        value = os.getenv("JWT_SECRET_KEY")
        if value is None:
            raise ValueError("JWT_SECRET_KEY is not set")
        return value

    def jwt_algorithm(self) -> str:
        value = os.getenv("JWT_ALGORITHM")
        if value is None:
            raise ValueError("JWT_ALGORITHM is not set")
        return value

    def jwt_expire_minutes(self) -> int:
        value = os.getenv("JWT_EXPIRE_MINUTES")
        if value is None:
            raise ValueError("JWT_EXPIRE_MINUTES is not set")
        try:
            return int(value)
        except ValueError:
            raise ValueError("JWT_EXPIRE_MINUTES is not a valid integer")

    def jwt_refresh_secret_key(self) -> str:
        value = os.getenv("JWT_REFRESH_SECRET_KEY")
        if value is None:
            raise ValueError("JWT_REFRESH_SECRET_KEY is not set")
        return value

    def jwt_refresh_algorithm(self) -> str:
        value = os.getenv("JWT_REFRESH_ALGORITHM")
        if value is None:
            raise ValueError("JWT_REFRESH_ALGORITHM is not set")
        return value

    def jwt_refresh_expire_minutes(self) -> int:
        value = os.getenv("JWT_REFRESH_EXPIRE_MINUTES")
        if value is None:
            raise ValueError("JWT_REFRESH_EXPIRE_MINUTES is not set")
        try:
            return int(value)
        except ValueError:
            raise ValueError("JWT_REFRESH_EXPIRE_MINUTES is not a valid integer")

    def postgresql_host(self) -> str:
        value = os.getenv("POSTGRESQL_HOST")
        if value is None:
            raise ValueError("POSTGRESQL_HOST is not set")
        return value

    def postgresql_port(self) -> str:
        value = os.getenv("POSTGRESQL_PORT")
        if value is None:
            raise ValueError("POSTGRESQL_PORT is not set")
        return value

    def postgresql_database(self) -> str:
        value = os.getenv("POSTGRESQL_DATABASE")
        if value is None:
            raise ValueError("POSTGRESQL_DATABASE is not set")
        return value

    def postgresql_user(self) -> str:
        value = os.getenv("POSTGRESQL_USER")
        if value is None:
            raise ValueError("POSTGRESQL_USER is not set")
        return value

    def postgresql_password(self) -> str:
        value = os.getenv("POSTGRESQL_PASSWORD")
        if value is None:
            raise ValueError("POSTGRESQL_PASSWORD is not set")
        return value

    def storage_path(self) -> str:
        value = os.getenv("STORAGE_PATH")
        if value is None:
            raise ValueError("STORAGE_PATH is not set")
        return value

    def coturn_secure_port(self) -> str:
        value = os.getenv("COTURN_SECURE_PORT")
        if value is None:
            raise ValueError("COTURN_SECURE_PORT is not set")
        return value

    def coturn_username(self) -> str:
        value = os.getenv("COTURN_USERNAME")
        if value is None:
            raise ValueError("COTURN_USERNAME is not set")
        return value

    def coturn_credential(self) -> str:
        value = os.getenv("COTURN_CREDENTIAL")
        if value is None:
            raise ValueError("COTURN_CREDENTIAL is not set")
        return value

    def coturn_secret(self) -> str:
        value = os.getenv("COTURN_SECRET")
        if value is None:
            raise ValueError("COTURN_SECRET is not set")
        return value

    def coturn_ttl(self) -> int:
        value = os.getenv("COTURN_TTL")
        if value is None:
            raise ValueError("COTURN_TTL is not set")
        try:
            return int(value)
        except ValueError:
            raise ValueError("COTURN_TTL is not a valid integer")

    def admin_client_id(self) -> str:
        value = os.getenv("ADMIN_CLIENT_ID")
        if value is None:
            raise ValueError("ADMIN_CLIENT_ID is not set")
        return value

    def admin_client_password(self) -> str:
        value = os.getenv("ADMIN_CLIENT_PASSWORD")
        if value is None:
            raise ValueError("ADMIN_CLIENT_PASSWORD is not set")
        return value
