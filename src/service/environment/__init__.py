from dotenv import load_dotenv
import os

class ServiceEnvironment:
    @staticmethod
    def load_env():
        load_dotenv()

    @staticmethod
    def get_JWT_SECRET():
        return os.getenv("JWT_SECRET")
