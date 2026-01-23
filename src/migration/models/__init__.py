from .person_snapshots import MigrationModelPersonSnapshot
from .camera_frames import MigrationModelCameraFrame

ALEMBIC_MODELS = [
    MigrationModelPersonSnapshot.metadata,
    MigrationModelCameraFrame.metadata,
]
