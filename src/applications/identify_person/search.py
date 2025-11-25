from repositories.database.person_features import RepositoryDatabasePersonFeatures
from modules.storage.person_image import ModuleStoragePersonImage
from repositories.database.person_image_paths import RepositoryDatabasePersonImagePaths
from entities.application.identify_person.search.conditions import EntityApplicationIdentifyPersonSearchConditions
from repositories.database.person_image_paths import RepositoryDatabasePersonImagePathsFilters
from entities.application.identify_person.search.return_value import EntityApplicationIdentifyPersonSearchReturnValue
from entities.environment.postgresql import EntityEnvironmentPostgreSQL
from entities.environment.storage import EntityEnvironmentStorage
from repositories.database import RepositoryDatabaseEngine
from repositories.database.person_features import RepositoryDatabasePersonFeaturesFilters
from repositories.database.person_features import RepositoryDatabasePersonFeaturesError
class ApplicationIdentifyPersonSearch:
    def __init__(
        self,
        database_person_image_paths: RepositoryDatabasePersonImagePaths,
        storage_person_image: ModuleStoragePersonImage,
        database_person_features: RepositoryDatabasePersonFeatures,
        ):
        self.database_person_image_paths = database_person_image_paths
        self.database_person_features = database_person_features
        self.storage_person_image = storage_person_image

    @classmethod
    def create(
        cls,
        environment_postgresql: EntityEnvironmentPostgreSQL,
        environment_storage: EntityEnvironmentStorage,
    ) -> "ApplicationIdentifyPersonSearch":
        return cls(
            database_person_image_paths=RepositoryDatabasePersonImagePaths(RepositoryDatabaseEngine(
                host=environment_postgresql.host,
                port=environment_postgresql.port,
                user=environment_postgresql.user,
                password=environment_postgresql.password,
                database=environment_postgresql.database,
            )),
            storage_person_image=ModuleStoragePersonImage(environment_storage.path),
            database_person_features=RepositoryDatabasePersonFeatures(
                database=RepositoryDatabaseEngine(
                    host=environment_postgresql.host,
                    port=environment_postgresql.port,
                    user=environment_postgresql.user,
                    password=environment_postgresql.password,
                    database=environment_postgresql.database,
                )),
            )

    def search(self, conditions: EntityApplicationIdentifyPersonSearchConditions) -> list[EntityApplicationIdentifyPersonSearchReturnValue]:
        person_image_paths = self.database_person_image_paths.find_all(
            RepositoryDatabasePersonImagePathsFilters(
                timestamp_after=conditions.after,
                timestamp_before=conditions.before,
                view_ids=conditions.view_ids,
                camera_ids=conditions.camera_ids,
                image_ids=conditions.image_ids,
            )
        )
        return_values = []
        for person_image_path in person_image_paths:
            print(person_image_path.image_id)
            try:
                return_values.append(EntityApplicationIdentifyPersonSearchReturnValue(
                        image_id=person_image_path.image_id,
                        person_id=self.database_person_features.find_first(
                            RepositoryDatabasePersonFeaturesFilters(
                                image_ids=[person_image_path.image_id]
                            )
                        ).person_id,
                        camera_id=person_image_path.camera_id,
                        view_id=person_image_path.view_id,
                        timestamp=person_image_path.timestamp,
                    )
                )
            except RepositoryDatabasePersonFeaturesError:
                continue
        return return_values
