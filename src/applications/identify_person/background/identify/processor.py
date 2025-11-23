from repositories.database.person_features import RepositoryDatabasePersonFeatures
from repositories.database.person_features import RepositoryDatabasePersonFeaturesFilters
from repositories.database.person_features import RepositoryDatabasePersonFeatureOrderings
from modules.reid.identifier import ModuleReIDIdentifier
import uuid
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from repositories.database import RepositoryDatabaseEngine

class ApplicationIdentifyPersonBackgroundIdentifyProcessor:
    def __init__(
        self,
        database_person_features: RepositoryDatabasePersonFeatures,
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
            database_person_features=RepositoryDatabasePersonFeatures(
                database=RepositoryDatabaseEngine(
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
        query_person_feature = self.database_person_features.find_first(
            RepositoryDatabasePersonFeaturesFilters(id=id)
        )
        gallery_person_feature = self.database_person_features.find_first(
            RepositoryDatabasePersonFeaturesFilters(
                feature=query_person_feature.feature,
                timestamp_before=query_person_feature.timestamp,
            ),
            RepositoryDatabasePersonFeatureOrderings(feature_to_nearest=query_person_feature.feature),
        )
        if not self.reid_identifier.identify(query_person_feature.feature, gallery_person_feature.feature):
            return
        query_person_feature.person_id = gallery_person_feature.person_id
        self.database_person_features.merge(query_person_feature)
