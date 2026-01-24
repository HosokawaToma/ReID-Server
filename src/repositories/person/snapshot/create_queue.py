from repositories.utils.redis import RepositoryUtilRedis
from repositories.utils.redis import RepositoryUtilRedisKey
from repositories.utils.database import RepositoryUtilDatabase
from repositories.utils.storage import RepositoryUtilStorage
from repositories.utils.storage.paths.camera_frame import RepositoryUtilStoragePathCameraFrame
from domain.camera_frame.image import DomainCameraFrameImage
from domain.id import DomainId
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.image import DomainImage
from migration.models.camera_frames import MigrationModelCameraFrame
from environment import Environment
from error import Error
from uuid import UUID

class RepositoryPersonSnapshotCreateQueueError(Error):
    pass

class RepositoryPersonSnapshotCreateQueuePushError(RepositoryPersonSnapshotCreateQueueError):
    pass

class RepositoryPersonSnapshotCreateQueuePopError(RepositoryPersonSnapshotCreateQueueError):
    pass


class RepositoryPersonSnapshotCreateQueue:
    def __init__(
        self,
        redis: RepositoryUtilRedis,
        database: RepositoryUtilDatabase,
        storage: RepositoryUtilStorage,
    ):
        self.redis = redis
        self.database = database
        self.storage = storage

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryPersonSnapshotCreateQueue":
        return cls(
            redis=RepositoryUtilRedis.create(environment),
            database=RepositoryUtilDatabase.create(environment),
            storage=RepositoryUtilStorage.create(environment),
        )

    def _model_to_domain(self, model: MigrationModelCameraFrame, image: DomainImage) -> DomainCameraFrameImage:
        return DomainCameraFrameImage(
            id=DomainId(id=model.id),
            location=DomainLocation(camera_id=model.camera_id, view_id=model.view_id),
            timestamp=DomainTimestamp(timestamp=model.timestamp),
            image=image,
        )

    def _domain_to_model(self, domain: DomainCameraFrameImage) -> MigrationModelCameraFrame:
        return MigrationModelCameraFrame(
            id=domain.id.id,
            camera_id=domain.location.camera_id,
            view_id=domain.location.view_id,
            timestamp=domain.timestamp.timestamp,
        )

    def push(self, frame_image: DomainCameraFrameImage) -> None:
        """
        画像を人物検出キューに追加します
        キューへの追加が失敗してもストレージとデータベースへの追加は行われます
        :param DomainCameraFrameImage frame_image: 画像
        :raise RepositoryPersonSnapshotCreateQueuePushError: 画像のキューへの追加が失敗した場合
        """
        try:
            with self.database as session:
                self.storage.save_image(
                    image=frame_image.image,
                    path=RepositoryUtilStoragePathCameraFrame(
                        id=frame_image.id,
                    ),
                )
                session.add(self._domain_to_model(frame_image))
            self.redis.push(
                key=RepositoryUtilRedisKey.PERSON_SNAPSHOT_CREATE,
                value={"id": str(frame_image.id)},
            )
        except Error as error:
            raise RepositoryPersonSnapshotCreateQueuePushError(error) from error


    def pop(self) -> DomainCameraFrameImage:
        try:
            data = self.redis.dequeue(RepositoryUtilRedisKey.PERSON_SNAPSHOT_CREATE)
            with self.database as session:
                query = session.query(MigrationModelCameraFrame)
                query = query.filter(MigrationModelCameraFrame.id == UUID(data["id"]))
                model = query.first()
                if model is None:
                    raise RepositoryPersonSnapshotCreateQueuePopError()
                image = self.storage.search_image(
                    path=RepositoryUtilStoragePathCameraFrame(
                        id=DomainId(id=model.id),
                    )
                )
                return self._model_to_domain(model, image)
        except Error as error:
            raise RepositoryPersonSnapshotCreateQueuePopError(error) from error
