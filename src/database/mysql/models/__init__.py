from .client import DatabaseMySQLModelClient
from .client_camera import DatabaseMySQLModelClientCamera

ALEMBIC_MODELS = [
    DatabaseMySQLModelClient.metadata,
    DatabaseMySQLModelClientCamera.metadata,
]
