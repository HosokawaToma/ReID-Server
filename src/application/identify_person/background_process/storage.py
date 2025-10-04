from pathlib import Path

from entities.identify_person.image import EntityIdentifyPersonImage


class ApplicationIdentifyPersonBackgroundProcessStorage:
    def __init__(self):
        self.path = Path("./results/identify_person")

    def save(self, identify_person_image: EntityIdentifyPersonImage) -> Path:
        directory = self.path / f"{identify_person_image.camera_id}" / f"{identify_person_image.view_id}" / f"{identify_person_image.person_id}"
        directory.mkdir(parents=True, exist_ok=True)

        filename = f"{identify_person_image.timestamp}_{identify_person_image.id}.jpg"
        filepath = directory / filename

        identify_person_image.image.save(filepath, "JPEG")
        return filepath
