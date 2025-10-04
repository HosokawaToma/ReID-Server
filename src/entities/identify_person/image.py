from datetime import datetime
from PIL import Image
import uuid
from pathlib import Path


class EntityIdentifyPersonImage:
    def __init__(
        self,
        client_id: int,
        image: Image,
        timestamp: datetime,
        camera_id: int = None,
        view_id: int = None,
        person_id: int = None,
        filepath: Path = None,
    ):
        self.id = uuid.uuid4()
        self.client_id = client_id
        self.image = image
        self.timestamp = timestamp
        self.camera_id = camera_id
        self.view_id = view_id
        self.person_id = person_id
        self.filepath = filepath
