from error import Error, NotFoundError
from environment import Environment
from repositories.utils.database import RepositoryUtilDatabase
from repositories.utils.storage import RepositoryUtilStorage
from repositories.utils.redis import RepositoryUtilRedis
from repositories.utils.redis import RepositoryUtilRedisKey
from repositories.utils.storage.paths.person_snapshot import RepositoryUtilStoragePathPersonSnapshot
from domain.person.snapshot.image import DomainPersonSnapshotImage
from domain.id import DomainId
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.person.id import DomainPersonId
from domain.id_sequence import DomainIdSequence
from domain.person.snapshot.image_sequence import DomainPersonSnapshotImageSequence
from domain.person.snapshot.feature import DomainPersonSnapshotFeature
from domain.person.feature import DomainPersonFeature
from migration.models.person_snapshots import MigrationModelPersonSnapshot
import torch


class RepositoryPersonSnapshotReidQueue:
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
    def create(cls, environment: Environment) -> "RepositoryPersonSnapshotReidQueue":
        return cls(
            redis=RepositoryUtilRedis.create(environment),
            database=RepositoryUtilDatabase.create(environment),
            storage=RepositoryUtilStorage.create(environment),
        )

    def push(self, person_snapshot: DomainPersonSnapshotImage) -> None:
        """
        人物検出結果を再識別キューに追加します
        キューへの追加が失敗してもデータベースへの追加は行われます
        :param DomainPersonSnapshotImage person_snapshot: 人物検出結果
        :raise RepositoryPersonSnapshotReidQueuePushError: キューへの追加が失敗した場合
        """
        self.storage.save_image(
            image=person_snapshot.image,
            path=RepositoryUtilStoragePathPersonSnapshot(
                id=person_snapshot.id,
            ),
        )
        with self.database as session:
            session.add(MigrationModelPersonSnapshot(
                id=person_snapshot.id.id,
                camera_id=person_snapshot.location.camera_id,
                view_id=person_snapshot.location.view_id,
                timestamp=person_snapshot.timestamp.timestamp,
                is_junk=person_snapshot.person_id.is_junk,
                person_id=person_snapshot.person_id.id.id if person_snapshot.person_id.id is not None else None,
                feature=person_snapshot.feature._feature.cpu().numpy().tolist(),
            ))
        self.redis.push(
            key=RepositoryUtilRedisKey.PERSON_SNAPSHOT_REID,
            value={"id": str(person_snapshot.id.id)},
        )

    def push_all(self, person_snapshot_images: DomainPersonSnapshotImageSequence) -> None:
        """
        人物検出結果を再識別キューに追加します
        キューへの追加が失敗してもデータベースへの追加は行われます
        :param DomainPersonSnapshotImageSequence person_snapshot_images: 人物検出結果のシーケンス
        :raise RepositoryPersonSnapshotReidQueuePushAllError: 人物検出結果のシーケンスの中でキューへの追加が失敗した場合
        """
        errors = []
        for person_snapshot_image in person_snapshot_images:
            try:
                self.push(person_snapshot_image)
            except Error as error:
                errors.append(error)
        if len(errors) > 0:
            raise errors[0]

    def push_id(self, id: DomainId) -> None:
        """
        人物検出結果を再識別キューに追加します
        キューへの追加が失敗してもデータベースへの追加は行われます
        :param DomainId id: 人物検出結果のID
        :raise RepositoryPersonSnapshotReidQueuePushIdError: キューへの追加が失敗した場合
        """
        self.redis.push(
            key=RepositoryUtilRedisKey.PERSON_SNAPSHOT_REID,
            value={"id": str(id.id)},
        )

    def push_ids(self, ids: DomainIdSequence) -> None:
        """
        人物検出結果を再識別キューに追加します
        キューへの追加が失敗してもデータベースへの追加は行われます
        :param DomainIdSequence ids: 人物検出結果のIDのシーケンス
        :raise RepositoryPersonSnapshotReidQueuePushIdsError: 人物検出結果のIDのシーケンスの中でキューへの追加が失敗した場合
        """
        errors = []
        for id in ids:
            try:
                self.push_id(id)
            except Error as error:
                errors.append(error)
        if len(errors) > 0:
            raise errors[0]

    def pop(self) -> DomainPersonSnapshotFeature:
        data = self.redis.dequeue(RepositoryUtilRedisKey.PERSON_SNAPSHOT_REID)
        with self.database as session:
            model = session.query(MigrationModelPersonSnapshot).filter(MigrationModelPersonSnapshot.id == data["id"]).first()
            if model is None:
                raise NotFoundError("人物検出結果が見つかりません")
            return DomainPersonSnapshotFeature(
                id=DomainId(id=model.id),
                location=DomainLocation(camera_id=model.camera_id, view_id=model.view_id),
                timestamp=DomainTimestamp(timestamp=model.timestamp),
                feature=DomainPersonFeature(feature=torch.tensor(model.feature)),
                person_id=DomainPersonId(
                    id=DomainId(id=model.person_id) if model.person_id is not None else None,
                    is_junk=model.is_junk,
                ),
            )
