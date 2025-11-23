from src.repositories.database.camera_clients import RepositoryDatabaseCameraClientModel
from src.repositories.database.person_image_paths import RepositoryDatabasePersonImagePathModel
from src.repositories.database.person_features import RepositoryDatabasePersonFeatureModel

ALEMBIC_MODELS = [
    RepositoryDatabaseCameraClientModel.metadata,
    RepositoryDatabasePersonImagePathModel.metadata,
    RepositoryDatabasePersonFeatureModel.metadata,
]
