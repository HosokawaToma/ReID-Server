"""
人物検出ジャンク判定キュー用リポジトリ

人物検出結果IDをジャンク判定キューに投入・取得する責務を持つ。
Redis・DB・ストレージを利用する。
"""
from repositories.utils.redis import RepositoryUtilRedis
from repositories.utils.redis import RepositoryUtilRedisKey
from repositories.utils.database import RepositoryUtilDatabase
from repositories.utils.storage import RepositoryUtilStorage
from repositories.utils.storage.paths.person_snapshot import RepositoryUtilStoragePathPersonSnapshot
from environment import Environment
from domain.id import DomainId
from domain.person.feature import DomainPersonFeature
from domain.person.snapshot.image import DomainPersonSnapshotImage
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.person.id import DomainPersonId
from domain.id_sequence import DomainIdSequence
from migration.models.person_snapshots import MigrationModelPersonSnapshot
from error import NotFoundError
from uuid import UUID
import torch


class RepositoryPersonSnapshotDetectJunkQueue:
    """
    人物検出ジャンク判定キュー用リポジトリクラス

    人物検出結果IDをキューに push/pop し、pop 時にストレージ・DB から
    人物検出画像ドメインを組み立てて返す。
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
    def create(cls, environment: Environment) -> "RepositoryPersonSnapshotDetectJunkQueue":
        """
        インスタンスを生成する。

        :param Environment environment: 環境変数
        :return RepositoryPersonSnapshotDetectJunkQueue: インスタンス
        """
        return cls(
            redis=RepositoryUtilRedis.create(environment),
            database=RepositoryUtilDatabase.create(environment),
            storage=RepositoryUtilStorage.create(environment),
        )

    def push(self, person_snapshot_id: DomainId) -> None:
        """
        人物検出結果IDをジャンク判定キューに1件追加する。

        :param DomainId person_snapshot_id: 人物検出結果のID
        """
        self.redis.push(
            key=RepositoryUtilRedisKey.PERSON_SNAPSHOT_DETECT_JUNK,
            value={"id": str(person_snapshot_id.id)},
        )

    def push_ids(self, ids: DomainIdSequence) -> None:
        """
        人物検出結果IDのシーケンスをジャンク判定キューに順次追加する。

        :param DomainIdSequence ids: 人物検出結果のIDのシーケンス
        """
        for id in ids:
            self.push(id)

    def pop(self) -> DomainPersonSnapshotImage:
        """
        ジャンク判定キューから1件取り出し、DB・ストレージから人物検出画像を組み立てて返す。

        :return DomainPersonSnapshotImage: 人物検出画像（特徴量・person_id・画像含む）
        :raises NotFoundError: キューで参照しているIDの人物検出結果がDBに存在しない場合
        """
        data = self.redis.dequeue(
            RepositoryUtilRedisKey.PERSON_SNAPSHOT_DETECT_JUNK)
        image = self.storage.search_image(
            path=RepositoryUtilStoragePathPersonSnapshot(
                id=DomainId(id=UUID(data["id"])),
            ),
        )
        with self.database as session:
            model = session.query(
                MigrationModelPersonSnapshot
            ).filter(
                MigrationModelPersonSnapshot.id == UUID(data["id"]),
            ).first()
            if model is None:
                raise NotFoundError("人物検出結果が見つかりません")
            return DomainPersonSnapshotImage(
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
                image=image,
            )
