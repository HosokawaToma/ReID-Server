"""
人物検出再識別キュー用リポジトリ

人物検出結果またはそのIDを再識別キューに投入・取得する責務を持つ。
Redis・DB・ストレージを利用する。
"""
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
    """
    人物検出再識別キュー用リポジトリクラス

    人物検出結果（画像付き）またはIDをキューに push し、pop 時に
    DB から人物検出特徴ドメイン（画像なし）を組み立てて返す。
    """

    def __init__(
        self,
        redis: RepositoryUtilRedis,
        database: RepositoryUtilDatabase,
        storage: RepositoryUtilStorage,
    ):
        """
        :param RepositoryUtilRedis redis: Redis ユーティリティ
        :param RepositoryUtilDatabase database: データベースユーティリティ
        :param RepositoryUtilStorage storage: ストレージユーティリティ
        """
        self.redis = redis
        self.database = database
        self.storage = storage

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryPersonSnapshotReidQueue":
        """
        インスタンスを生成する。

        :param Environment environment: 環境設定
        :return RepositoryPersonSnapshotReidQueue: インスタンス
        """
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
        :raises InternalServerError: キュー・ストレージ・DB への追加が失敗した場合
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
        :raises InternalServerError: シーケンスのいずれかでキュー・ストレージ・DB への追加が失敗した場合
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
        :raises InternalServerError: キューへの追加が失敗した場合
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
        :raises InternalServerError: シーケンスのいずれかでキューへの追加が失敗した場合
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
        """
        再識別キューから1件取り出し、DBから人物検出特徴（画像なし）を組み立てて返す。

        :return DomainPersonSnapshotFeature: 人物検出特徴（ID・位置・時刻・特徴量・person_id）
        :raises NotFoundError: キューで参照しているIDの人物検出結果がDBに存在しない場合
        """
        data = self.redis.dequeue(RepositoryUtilRedisKey.PERSON_SNAPSHOT_REID)
        with self.database as session:
            model = session.query(MigrationModelPersonSnapshot).filter(
                MigrationModelPersonSnapshot.id == data["id"]).first()
            if model is None:
                raise NotFoundError("人物検出結果が見つかりません")
            return DomainPersonSnapshotFeature(
                id=DomainId(id=model.id),
                location=DomainLocation(
                    camera_id=model.camera_id, view_id=model.view_id),
                timestamp=DomainTimestamp(timestamp=model.timestamp),
                feature=DomainPersonFeature(
                    feature=torch.tensor(model.feature)),
                person_id=DomainPersonId(
                    id=DomainId(
                        id=model.person_id) if model.person_id is not None else None,
                    is_junk=model.is_junk,
                ),
            )
