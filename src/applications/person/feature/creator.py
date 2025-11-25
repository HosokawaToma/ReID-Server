from modules.reid.model import ModuleReIDModel
from repositories.database.person_features import RepositoryDatabasePersonFeatures

from entities.person_image import EntityPersonImage
from entities.person_feature import EntityPersonFeature

class ApplicationPersonFeatureCreator:
    def __init__(
        self,
        reid_model: ModuleReIDModel,
        database_person_features: RepositoryDatabasePersonFeatures,
    ):
        self.reid_model = reid_model
        self.database_person_features = database_person_features

    def create(self, person_image: EntityPersonImage) -> EntityPersonFeature:
        person_feature = EntityPersonFeature(
            image_id=person_image.id,
            feature=self.reid_model.extract_feature(
                person_image.image,
                person_image.camera_id,
                person_image.view_id,
            ),
            camera_id=person_image.camera_id,
            view_id=person_image.view_id,
            timestamp=person_image.timestamp,
        )
        self.database_person_features.add(person_feature)
        return person_feature
