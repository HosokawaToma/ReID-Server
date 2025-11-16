from modules.database.person_features import ModuleDatabasePersonFeatures
from modules.storage.person_image import ModuleStoragePersonImage
from modules.database.person_image_paths import ModuleDatabasePersonImagePaths
from entities.application.identify_person.search.conditions import EntityApplicationIdentifyPersonSearchConditions
from entities.database.where.person_image_paths import EntityDatabaseWherePersonImagePath
from entities.database.where.person_features import EntityDatabaseWherePersonFeatures
from entities.application.identify_person.search.return_value import EntityApplicationIdentifyPersonSearchReturnValue

class ApplicationIdentifyPersonSearch:
    def __init__(
        self,
        database_person_image_paths: ModuleDatabasePersonImagePaths,
        storage_person_image: ModuleStoragePersonImage,
        database_person_features: ModuleDatabasePersonFeatures,
        ):
        self.database_person_image_paths = database_person_image_paths
        self.database_person_features = database_person_features
        self.storage_person_image = storage_person_image

    async def search(self, conditions: EntityApplicationIdentifyPersonSearchConditions):
        person_image_paths = self.database_person_image_paths.select(EntityDatabaseWherePersonImagePath(
            after=conditions.after,
            before=conditions.before,
            view_ids=conditions.view_ids,
            camera_ids=conditions.camera_ids,
        ))
        return_values = []
        for person_image_path in person_image_paths:
            return_values.append(EntityApplicationIdentifyPersonSearchReturnValue(
                image=self.storage_person_image.search(person_image_path).image,
                person_id=self.database_person_features.select_one(EntityDatabaseWherePersonFeatures(
                    image_ids=[person_image_path.image_id],
                )).person_id,
                camera_id=person_image_path.camera_id,
                view_id=person_image_path.view_id,
                timestamp=person_image_path.timestamp,
            ))
        return return_values
