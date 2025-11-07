import os
from entities.image import EntityImage

class ModuleStorageImage:
    IMAGE_PATH = "{storage_path}/{camera_id}/{view_id}/{timestamp}_{id}.jpg"

    def __init__(self, storage_path: str):
        self.storage_path = storage_path

    def save(self, image: EntityImage) -> None:
        path = self.IMAGE_PATH.format(
            camera_id=image.camera_id,
            view_id=image.view_id,
            timestamp=image.timestamp.strftime("%Y%m%d%H%M%S"),
            id=image.id
        )
        os.makedirs(os.path.dirname(path), exist_ok=True)
        image.image.save(path)
