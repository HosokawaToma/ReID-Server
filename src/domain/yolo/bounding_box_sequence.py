from dataclasses import dataclass
from domain.yolo.bounding_box import DomainYoloBoundingBox
from domain.utils.sequence_base import DomainUtilsSequenceBase
from domain.camera_frame.image import DomainCameraFrameImage
from domain.person.snapshot.image_sequence import DomainPersonSnapshotImageSequence
from domain.id import DomainId
from domain.person.id import DomainPersonId
from domain.person.snapshot.image import DomainPersonSnapshotImage

@dataclass(frozen=True)
class DomainYoloBoundingBoxSequence(DomainUtilsSequenceBase[DomainYoloBoundingBox]):
    """
    YOLOのバウンディングボックスのシーケンスのドメインモデル
    """

    def create_person_snapshot_images(self, camera_frame_image: DomainCameraFrameImage) -> DomainPersonSnapshotImageSequence:
        return DomainPersonSnapshotImageSequence(items=[
            DomainPersonSnapshotImage(
                id=DomainId(),
                location=camera_frame_image.location,
                timestamp=camera_frame_image.timestamp,
                image=bounding_box.crop(camera_frame_image.image),
                person_id=DomainPersonId(),
            ) for bounding_box in self
        ])
