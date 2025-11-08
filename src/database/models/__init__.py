from .camera_client import DatabaseModelCameraClient
from .person_feature import DatabaseModelPersonFeature

ALEMBIC_MODELS = [
    DatabaseModelCameraClient.metadata,
    DatabaseModelPersonFeature.metadata,
]
