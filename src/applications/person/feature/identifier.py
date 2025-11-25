from repositories.database.person_features import RepositoryDatabasePersonFeatures
from repositories.database.person_features import RepositoryDatabasePersonFeaturesFilters
from repositories.database.person_features import RepositoryDatabasePersonFeatureOrderings
from entities.person_feature import EntityPersonFeature
from modules.reid.identifier import ModuleReIDIdentifier

class ApplicationPersonFeatureIdentifier:
    def __init__(
        self,
        database_person_features: RepositoryDatabasePersonFeatures,
        reid_identifier: ModuleReIDIdentifier,
    ):
        self.database_person_features = database_person_features
        self.reid_identifier = reid_identifier

    def identify(self, person_feature: EntityPersonFeature) -> None:
        gallery_person_feature = self.database_person_features.find_first(
            RepositoryDatabasePersonFeaturesFilters(
                timestamp_before=person_feature.timestamp,
            ),
            RepositoryDatabasePersonFeatureOrderings(
                feature_to_nearest=person_feature.feature,
            ),
        )
        self.reid_identifier.guarantee(
            person_feature.feature,
            gallery_person_feature.feature,
        )
        person_feature.person_id = gallery_person_feature.person_id
        self.database_person_features.merge(person_feature)
