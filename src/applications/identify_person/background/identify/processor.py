from modules.database.person_features import ModuleDatabasePersonFeatures
from modules.reid.identifier import ModuleReIDIdentifier
import uuid
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from database import Database

class ApplicationIdentifyPersonBackgroundIdentifyProcessor:
    def __init__(
        self,
        database_person_features: ModuleDatabasePersonFeatures,
        reid_identifier: ModuleReIDIdentifier,
    ):
        self.database_person_features = database_person_features
        self.reid_identifier = reid_identifier

    @classmethod
    def create(
        cls,
        environment_postgresql: EntityEnvironmentPostgreSQL,
    ):
        return cls(
            database_person_features=ModuleDatabasePersonFeatures(
                database=Database(
                    host=environment_postgresql.host,
                    port=environment_postgresql.port,
                    user=environment_postgresql.user,
                    password=environment_postgresql.password,
                    database=environment_postgresql.database,
                )
            ),
            reid_identifier=ModuleReIDIdentifier(threshold=0.9),
        )

    async def process(self, id: uuid.UUID):
        query_person_feature = self.database_person_features.select_by_id(id)
        gallery_person_features = self.database_person_features.select_top_one_by_before_timestamp(
            query_person_feature.feature, query_person_feature.timestamp)
        if gallery_person_features is None:
            return
        if not self.reid_identifier.identify(query_person_feature.feature, gallery_person_features.feature):
            return
        query_person_feature.person_id = gallery_person_features.person_id
        self.database_person_features.update(query_person_feature)
