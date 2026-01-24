from environment import Environment
from applications import ApplicationBase
from repositories.person.snapshot.create_queue import RepositoryPersonSnapshotCreateQueue
from dto.location import DtoLocation
from dto.timestamp import DtoTimestamp
from dto.image import DtoImage
from domain.camera_frame.image import DomainCameraFrameImage
from domain.id import DomainId
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.image import DomainImage


class ApplicationPersonSnapshotCreate(ApplicationBase):
    def __init__(
        self,
        repository_person_snapshot_create_queue: RepositoryPersonSnapshotCreateQueue,
    ):
        self.repository_person_snapshot_create_queue = repository_person_snapshot_create_queue

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonSnapshotCreate":
        return cls(
            repository_person_snapshot_create_queue=RepositoryPersonSnapshotCreateQueue.create(environment),
        )

    def save(self, location: DtoLocation, timestamp: DtoTimestamp, image: DtoImage) -> None:
        """
        人物検出を保存する
        :param DtoLocation location: 人物検出の位置
        :param DtoTimestamp timestamp: 人物検出の時間
        :param DtoImage image: 人物検出の画像
        :raises InternalServerError: 人物検出保存に失敗した場合に発生するエラー
        """
        self.repository_person_snapshot_create_queue.push(DomainCameraFrameImage(
            id=DomainId(),
            location=DomainLocation(camera_id=location.camera_id, view_id=location.view_id),
            timestamp=DomainTimestamp(timestamp=timestamp.timestamp),
            image=DomainImage(bytes=image.bytes, format=image.format),
        ))
