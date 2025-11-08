from database.postgresql import DatabasePostgreSQL
from entities.person_feature import EntityPersonFeature

class ModuleDatabasePostgreSQLPersonFeatures:
    NAME = "person_features"
    CAMERA_ID_KEY_OF_METADATA = "camera_id"
    VIEW_ID_KEY_OF_METADATA = "view_id"
    TIMESTAMP_KEY_OF_METADATA = "timestamp"

    def __init__(
        self,
        database_postgresql: DatabasePostgreSQL
        ):
        self.database_postgresql = database_postgresql

    def insert(self, person_feature: EntityPersonFeature) -> None:
        with self.database_postgresql as db_session:
            db_session.add(person_feature.to_database_model())
