import os
from dotenv import load_dotenv


class ApplicationEnvironment:
    def __init__(self):
        load_dotenv()

    def get_server_ip(self):
        return os.getenv("STUN_SERVER_IP")

    def get_turn_username(self):
        return os.getenv("TURN_USERNAME")

    def get_turn_password(self):
        return os.getenv("TURN_PASSWORD")

    def get_jwt_secret_key(self):
        return os.getenv("JWT_SECRET_KEY")

    def get_jwt_algorithm(self):
        return os.getenv("JWT_ALGORITHM")
