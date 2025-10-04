from modules.database import ModuleDatabase
from entities.identify_person.image import EntityIdentifyPersonImage
from migration.models.person_crop_images import PersonCropImages

class ApplicationIdentifyPersonBackgroundProcessDatabase(ModuleDatabase):
    def __init__(self):
        super().__init__()

    def insert_identify_person_image(self, person_crop_image: EntityIdentifyPersonImage):
        person_crop_image_model = PersonCropImages(
            id=str(person_crop_image.id),
            person_id=person_crop_image.person_id,
            camera_id=person_crop_image.camera_id,
            view_id=person_crop_image.view_id,
            image_path=str(person_crop_image.filepath),
            timestamp=person_crop_image.timestamp,
        )
        self.add(person_crop_image_model)
        self.commit()
