from modules.storage.person_image import ModuleStoragePersonImage
from repositories.database.person_image_paths import RepositoryDatabasePersonImagePaths
from repositories.database.person_image_paths import RepositoryDatabasePersonImagePathsFilters
import uuid
from entities.environment.storage import EntityEnvironmentStorage
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from repositories.database import RepositoryDatabaseEngine
import io

class ApplicationPersonImages:
    def __init__(
        self,
        module_database_person_image_paths: RepositoryDatabasePersonImagePaths,
        storage_person_image: ModuleStoragePersonImage,
    ):
        self.module_database_person_image_paths = module_database_person_image_paths
        self.storage_person_image = storage_person_image

    @classmethod
    def create(
        cls,
        environment_storage: EntityEnvironmentStorage,
        environment_postgresql: EntityEnvironmentPostgreSQL,
    ) -> "ApplicationPersonImages":
        return cls(
            module_database_person_image_paths=RepositoryDatabasePersonImagePaths(RepositoryDatabaseEngine(
                host=environment_postgresql.host,
                port=environment_postgresql.port,
                user=environment_postgresql.user,
                password=environment_postgresql.password,
                database=environment_postgresql.database,
            )),
            storage_person_image=ModuleStoragePersonImage(environment_storage.path),
        )

    def search(self, image_id: uuid.UUID) -> io.BytesIO:
        img_buffer = io.BytesIO()
        person_image = self.storage_person_image.search(
            self.module_database_person_image_paths.find_first(filters=RepositoryDatabasePersonImagePathsFilters(image_ids=[image_id]))
        )
        person_image.image.save(img_buffer, format="JPEG")
        img_buffer.seek(0)
        return img_buffer
