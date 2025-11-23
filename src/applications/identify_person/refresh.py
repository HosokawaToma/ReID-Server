from datetime import datetime
from modules.storage.person_image import ModuleStoragePersonImage
from modules.database.person_image_paths import ModuleDatabasePersonImagePaths
from collections.person_image_paths import CollectionPersonImagePaths, CollectionPersonImagePathsFilter
from entities.person_image_path import EntityPersonImagePath
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from entities.environment.storage import EntityEnvironmentStorage
from database import Database

class ApplicationIdentifyPersonRefresh:
    def __init__(
        self,
        module_storage_person_image: ModuleStoragePersonImage,
        module_database_person_image_paths: ModuleDatabasePersonImagePaths,
        ):
        self.module_storage_person_image = module_storage_person_image
        self.module_database_person_image_paths = module_database_person_image_paths

    @classmethod
    def create(
        cls,
        environment_postgresql: EntityEnvironmentPostgreSQL,
        environment_storage: EntityEnvironmentStorage,
    ):
        return cls(
            module_storage_person_image=ModuleStoragePersonImage(environment_storage.path),
            module_database_person_image_paths=ModuleDatabasePersonImagePaths(
                database=Database(
                    host=environment_postgresql.host,
                    port=environment_postgresql.port,
                    user=environment_postgresql.user,
                    password=environment_postgresql.password,
                    database=environment_postgresql.database,
                )
            )
        )

    def refresh_person_image_paths(
        self,
        after_timestamp: datetime | None,
        before_timestamp: datetime | None,
        camera_ids: list[int] | None,
        view_ids: list[int] | None,
    ) -> list[EntityPersonImagePath]:
        person_image_paths = CollectionPersonImagePaths(
            self.module_storage_person_image.get_all_paths()
        ).filter(
            CollectionPersonImagePathsFilter(
                after_timestamp=after_timestamp,
                before_timestamp=before_timestamp,
                camera_ids=camera_ids,
                view_ids=view_ids,
            )
        ).items
        self.module_database_person_image_paths.update_all(person_image_paths)
        return person_image_paths
