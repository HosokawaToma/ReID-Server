from modules.storage.person_image import ModuleStoragePersonImage
from modules.database.person_image_paths import ModuleDatabasePersonImagePaths
from entities.person_image import EntityPersonImage
import uuid
from entities.environment.storage import EntityEnvironmentStorage
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from database import Database
import io

class ApplicationPersonImages:
    def __init__(
        self,
        module_database_person_image_paths: ModuleDatabasePersonImagePaths,
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
            module_database_person_image_paths=ModuleDatabasePersonImagePaths(Database(
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
        self.storage_person_image.search(
            self.module_database_person_image_paths.select_by_image_id(image_id)).image.save(img_buffer, format="JPEG")
        img_buffer.seek(0)
        return img_buffer
