from .camera_client import DatabaseModelCameraClient
from .person_feature import DatabaseModelPersonFeature
from .person_image_path import DatabaseModelPersonImagePath

ALEMBIC_MODELS = [
    DatabaseModelCameraClient.metadata,
    DatabaseModelPersonFeature.metadata,
    DatabaseModelPersonImagePath.metadata,
]
