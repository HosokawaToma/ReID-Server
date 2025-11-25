from .camera_clients import MigrationModelCameraClient
from .person_image_paths import MigrationModelPersonImagePath
from .person_features import MigrationModelPersonFeature

ALEMBIC_MODELS = [
    MigrationModelCameraClient.metadata,
    MigrationModelPersonImagePath.metadata,
    MigrationModelPersonFeature.metadata,
]
