from pathlib import Path
import io

from entities.person_crop_image import EntityPersonCropImage


class ServiceStoragePersonCropImages:
    path = Path("./results/identify_person")  # 適切なパスに変更

    @staticmethod
    def save(person_crop_image: EntityPersonCropImage) -> Path:
        directory = ServiceStoragePersonCropImages.path / f"{person_crop_image.camera_id}" / f"{person_crop_image.view_id}" / f"{person_crop_image.person_id}"
        directory.mkdir(parents=True, exist_ok=True)

        filename = f"{person_crop_image.timestamp}_{person_crop_image.id}.jpg"
        filepath = directory / filename

        person_crop_image.image.save(filepath, "JPEG")
        return filepath
