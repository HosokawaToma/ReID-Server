from .camera_clients import MigrationModelCameraClient
from .person_snapshots import MigrationModelPersonSnapshot

ALEMBIC_MODELS = [
    MigrationModelCameraClient.metadata,
    MigrationModelPersonSnapshot.metadata,
]
