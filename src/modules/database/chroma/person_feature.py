from database.chroma import DatabaseChroma
from entities.person_feature import EntityPersonFeature

class ModuleDatabaseChromaPersonFeature:
    NAME = "person_feature"
    CAMERA_ID_KEY_OF_METADATA = "camera_id"
    VIEW_ID_KEY_OF_METADATA = "view_id"
    TIMESTAMP_KEY_OF_METADATA = "timestamp"

    def __init__(
        self,
        database_chroma: DatabaseChroma
        ):
        self.database_chroma = database_chroma

    def insert(self, person_feature: EntityPersonFeature) -> None:
        self.database_chroma(self.NAME).add(
            embeddings=[person_feature.feature],
            metadatas=[
                {
                    self.CAMERA_ID_KEY_OF_METADATA: person_feature.camera_id,
                    self.VIEW_ID_KEY_OF_METADATA: person_feature.view_id,
                    self.TIMESTAMP_KEY_OF_METADATA: person_feature.timestamp,
                }
            ],
            ids=[person_feature.id],
        )
