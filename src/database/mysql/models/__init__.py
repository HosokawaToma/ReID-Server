from .camera_client import DatabaseMySQLModelCameraClient
from .client import DatabaseMySQLModelClient

ALEMBIC_MODELS = [
    DatabaseMySQLModelCameraClient.metadata,
    DatabaseMySQLModelClient.metadata,
]
