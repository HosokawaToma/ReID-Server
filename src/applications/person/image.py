import uuid
from datetime import datetime
from typing import List
from dataclasses import dataclass

from repositories.database.person_image_paths import RepositoryDatabasePersonImagePaths
from repositories.database.person_image_paths import RepositoryDatabasePersonImagePathsFilters
from repositories.database.person_image_paths import RepositoryDatabasePersonImagePathsOrderings
from repositories.storage.person_images import RepositoryStoragePersonImages
from sequences.person_image_paths import SequencePersonImagePaths

from entities.person_image import EntityPersonImage

@dataclass
class ApplicationPersonImageSearchFilters:
    ids: list[uuid.UUID] | None = None
    view_ids: list[int] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None

@dataclass
class ApplicationPersonImageSearchOrderings:
    timestamp_descending: bool | None = None
    timestamp_ascending: bool | None = None

class ApplicationPersonImage:
    def __init__(
        self,
        repository_person_image_paths: RepositoryDatabasePersonImagePaths,
        repository_person_images: RepositoryStoragePersonImages,
    ):
        self.repository_person_image_paths = repository_person_image_paths
        self.repository_person_images  = repository_person_images

    def search_one(
        self,
        filters: ApplicationPersonImageSearchFilters | None = None,
        orderings: ApplicationPersonImageSearchOrderings | None = None,
    ) -> EntityPersonImage:
        person_image_path = self.repository_person_image_paths.find_first(
            filters=RepositoryDatabasePersonImagePathsFilters(
                image_ids=filters.ids if filters is not None else None,
                view_ids=filters.view_ids if filters is not None else None,
                timestamp_after=filters.timestamp_after if filters is not None else None,
                timestamp_before=filters.timestamp_before if filters is not None else None,
            ),
            orderings=RepositoryDatabasePersonImagePathsOrderings(
                timestamp_descending=orderings.timestamp_descending if orderings is not None else None,
                timestamp_ascending=orderings.timestamp_ascending if orderings is not None else None,
            ),
        )
        return self.repository_person_images.search_one(person_image_path)
