import os
from entities.image import EntityImage

class ModuleStorageImage:
    IMAGE_PATH = "{storage_path}/{camera_id}/{view_id}/{timestamp}_{id}.jpg"

    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)

    def save(self, image: EntityImage) -> None:
        path = self.IMAGE_PATH.format(
            camera_id=image.camera_id,
            view_id=image.view_id,
            timestamp=image.timestamp.isoformat(),
            id=image.id
        )
        image.image.save(path)
