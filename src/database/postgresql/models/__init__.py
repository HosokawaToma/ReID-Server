from .camera_client import DatabasePostgreSQLModelCameraClient
from .person_feature import DatabasePostgreSQLModelPersonFeature

ALEMBIC_MODELS = [
    DatabasePostgreSQLModelCameraClient.metadata,
    DatabasePostgreSQLModelPersonFeature.metadata,
]
