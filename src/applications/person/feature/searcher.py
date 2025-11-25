from dataclasses import dataclass
from datetime import datetime
import uuid

from repositories.database.person_features import RepositoryDatabasePersonFeatures
from repositories.database.person_features import RepositoryDatabasePersonFeaturesFilters
from repositories.database.person_features import RepositoryDatabasePersonFeatureOrderings
from entities.person_feature import EntityPersonFeature

@dataclass
class ApplicationPersonFeatureSearchFilters:
    ids: list[uuid.UUID] | None = None
    camera_ids: list[int] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None

@dataclass
class ApplicationPersonFeatureSearchOrderings:
    timestamp_descending: bool | None = None
    timestamp_ascending: bool | None = None

class ApplicationPersonFeatureSearcher:
    def __init__(self, database_person_features: RepositoryDatabasePersonFeatures):
        self.database_person_features = database_person_features

    def search_one(
        self,
        filters: ApplicationPersonFeatureSearchFilters | None = None,
        orderings: ApplicationPersonFeatureSearchOrderings | None = None,
    ) -> EntityPersonFeature:
        return self.database_person_features.find_first(
            filters=RepositoryDatabasePersonFeaturesFilters(
                ids=filters.ids if filters is not None else None,
                camera_ids=filters.camera_ids if filters is not None else None,
                view_ids=filters.view_ids if filters is not None else None,
                timestamp_after=filters.timestamp_after if filters is not None else None,
                timestamp_before=filters.timestamp_before if filters is not None else None,
            ),
            orderings=RepositoryDatabasePersonFeatureOrderings(
                timestamp_descending=orderings.timestamp_descending if orderings is not None else None,
                timestamp_ascending=orderings.timestamp_ascending if orderings is not None else None,
            ),
        )
