from .person_snapshots import MigrationModelPersonSnapshot
from .frame_images import MigrationModelFrameImage

ALEMBIC_MODELS = [
    MigrationModelPersonSnapshot.metadata,
    MigrationModelFrameImage.metadata,
]
