import os

class Environment:

    def host(self) -> str:
        value = os.getenv("HOST")
        if value is None:
            raise ValueError("HOST is not set")
        return value

    def port(self) -> str:
        value = os.getenv("PORT")
        if value is None:
            raise ValueError("PORT is not set")
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

    def mysql_port(self) -> str:
        value = os.getenv("MYSQL_PORT")
        if value is None:
            raise ValueError("MYSQL_PORT is not set")
        return value

    def mysql_host(self) -> str:
        value = os.getenv("MYSQL_HOST")
        if value is None:
            raise ValueError("MYSQL_HOST is not set")
        return value

    def mysql_database(self) -> str:
        value = os.getenv("MYSQL_DATABASE")
        if value is None:
            raise ValueError("MYSQL_DATABASE is not set")
        return value

    def mysql_user(self) -> str:
        value = os.getenv("MYSQL_USER")
        if value is None:
            raise ValueError("MYSQL_USER is not set")
        return value

    def mysql_password(self) -> str:
        value = os.getenv("MYSQL_PASSWORD")
        if value is None:
            raise ValueError("MYSQL_PASSWORD is not set")
        return value

    def chroma_host(self) -> str:
        value = os.getenv("CHROMA_HOST")
        if value is None:
            raise ValueError("CHROMA_HOST is not set")
        return value

    def chroma_port(self) -> str:
        value = os.getenv("CHROMA_PORT")
        if value is None:
            raise ValueError("CHROMA_PORT is not set")
        return value

    def chroma_secret_token(self) -> str:
        value = os.getenv("CHROMA_SECRET_TOKEN")
        if value is None:
            raise ValueError("CHROMA_SECRET_TOKEN is not set")
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

    def coturn_password(self) -> str:
        value = os.getenv("COTURN_PASSWORD")
        if value is None:
            raise ValueError("COTURN_PASSWORD is not set")
        return value
