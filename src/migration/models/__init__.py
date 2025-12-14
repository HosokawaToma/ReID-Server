from .camera_clients import MigrationModelCameraClient
from .person_snapshots import MigrationModelPersonSnapshot
from .frame_image import MigrationModelFrameImage

ALEMBIC_MODELS = [
    MigrationModelCameraClient.metadata,
    MigrationModelPersonSnapshot.metadata,
    MigrationModelFrameImage.metadata,
]
