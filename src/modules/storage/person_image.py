import os
from entities.person_image import EntityPersonImage
from entities.person_image_path import EntityPersonImagePath
from errors.modules.storage.person_image import ErrorModuleStoragePersonImageNotFound
from PIL import Image

class ModuleStoragePersonImage:
    def __init__(self, storage_path: str):
        self.storage_path = storage_path

    def save(self, person_image: EntityPersonImage) -> EntityPersonImagePath:
        person_image_path = EntityPersonImagePath(
            image_id=person_image.id,
            camera_id=person_image.camera_id,
            view_id=person_image.view_id,
            timestamp=person_image.timestamp,
        )
        image_path = self.storage_path / person_image_path.path
        image_path.parent.mkdir(parents=True, exist_ok=True)
        person_image.image.save(image_path)
        return person_image_path

    def search(self, person_image_path: EntityPersonImagePath) -> EntityPersonImage:
        path = self.storage_path / person_image_path.path
        if not path.exists():
            raise ErrorModuleStoragePersonImageNotFound(f"Person image not found: {path}")
        try:
            image = Image.open(path)
            image.load()
            return EntityPersonImage(
                id=person_image_path.image_id,
                image=image,
                camera_id=person_image_path.camera_id,
                view_id=person_image_path.view_id,
                timestamp=person_image_path.timestamp,
            )
        except Exception as e:
            raise ErrorModuleStoragePersonImageNotFound(f"Error opening person image: {e}")
