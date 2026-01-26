from repositories.utils.database import RepositoryUtilDatabase
from error import NotFoundError
from environment import Environment
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshot
from repositories.utils.database.query.person_snapshot_answer_label import RepositoryUtilDatabaseQueryPersonSnapshotAnswerLabel
from domain.id_sequence import DomainIdSequence
from domain.id import DomainId
from migration.models.person_snapshots import MigrationModelPersonSnapshot
from migration.models.person_snapshots_answer_labels import MigrationModelPersonSnapshotsAnswerLabels
from domain.person.snapshot.detail import DomainPersonSnapshotDetail
from domain.person.snapshot.detail_sequence import DomainPersonSnapshotDetailSequence
from domain.location import DomainLocation
from domain.timestamp import DomainTimestamp
from domain.person.id import DomainPersonId
from domain.person.feature import DomainPersonFeature
from domain.person.snapshot.feature import DomainPersonSnapshotFeature
from domain.person.snapshot.person_id import DomainPersonSnapshotPersonId
from domain.person.snapshot.person_id_sequence import DomainPersonSnapshotPersonIdSequence
import torch
import uuid

class RepositoryPersonSnapshot:
    def __init__(self, database: RepositoryUtilDatabase):
        self.database = database

    @classmethod
    def create(cls, environment: Environment) -> "RepositoryPersonSnapshot":
        return cls(database=RepositoryUtilDatabase.create(environment))

    def find_ids(self, query: RepositoryUtilDatabaseQueryPersonSnapshot | None = None) -> DomainIdSequence:
        with self.database as session:
            session_query = session.query(MigrationModelPersonSnapshot)
            if query is not None:
                session_query = query.build(session_query)
            models = session_query.all()
            return DomainIdSequence(items=[DomainId(id=model.id) for model in models])

    def find_details(self, query: RepositoryUtilDatabaseQueryPersonSnapshot | None = None) -> DomainPersonSnapshotDetailSequence:
        with self.database as session:
            session_query = session.query(MigrationModelPersonSnapshot)
            if query is not None:
                session_query = query.build(session_query)
            models = session_query.all()
            return DomainPersonSnapshotDetailSequence(items=[
                DomainPersonSnapshotDetail(
                    id=DomainId(id=model.id),
                    location=DomainLocation(camera_id=model.camera_id, view_id=model.view_id),
                    timestamp=DomainTimestamp(timestamp=model.timestamp),
                    person_id=DomainPersonId(
                        id=DomainId(id=model.person_id) if model.person_id is not None else None,
                        is_junk=model.is_junk,
                    ),
                ) for model in models])

    def find_features_by_nearest(self, person_snapshot: DomainPersonSnapshotFeature) -> DomainPersonSnapshotFeature:
        """
        同じ日付で過去に検出された特徴量が最も近い人物検出結果を取得します
        :param DomainPersonSnapshotFeature person_snapshot: 人物検出結果
        :return DomainPersonSnapshotFeature: 特徴量が最も近い人物検出結果
        :raise NotFoundError: 特徴量が最も近い人物検出結果が見つからない場合
        :raise NotFoundError: 特徴量が最も近い人物検出結果の特徴量が存在しない場合
        """
        with self.database as session:
            query = session.query(MigrationModelPersonSnapshot)
            query = query.filter(MigrationModelPersonSnapshot.timestamp <= person_snapshot.timestamp.timestamp)
            query = query.filter(MigrationModelPersonSnapshot.timestamp >= person_snapshot.timestamp.today().timestamp)
            query = query.filter(MigrationModelPersonSnapshot.is_junk.is_(False))
            query = query.filter(MigrationModelPersonSnapshot.feature.isnot(None))
            query = query.order_by(MigrationModelPersonSnapshot.feature.op("<=>")(person_snapshot.feature.value.cpu().numpy().tolist()))
            model = query.first()
            if model is None:
                raise NotFoundError("特徴量が最も近い人物検出結果が見つかりません")
            if model.feature is None:
                raise NotFoundError("特徴量が最も近い人物検出結果の特徴量が存在しません")
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

    def find_answer_labels(self, query: RepositoryUtilDatabaseQueryPersonSnapshotAnswerLabel | None = None) -> DomainPersonSnapshotPersonIdSequence:
        """
        人物検出結果の正解ラベルを検索する
        :param RepositoryUtilDatabaseQueryPersonSnapshotAnswerLabel query: クエリ
        :return DomainPersonSnapshotPersonIdSequence: 人物検出結果の正解ラベルリスト
        :raises NotFoundError: 人物検出結果の正解ラベルが見つからない場合
        """
        with self.database as session:
            session_query = session.query(MigrationModelPersonSnapshotsAnswerLabels)
            if query is not None:
                session_query = query.build(session_query)
            models = session_query.all()
            return DomainPersonSnapshotPersonIdSequence(items=[DomainPersonSnapshotPersonId(
                id=DomainId(id=model.person_snapshot_id),
                person_id=DomainPersonId(
                    id=DomainId(id=model.person_id) if model.person_id is not None else None,
                    is_junk=model.is_junk,
                ),
            ) for model in models])

    def find_answer_label_kinds(self) -> DomainPersonSnapshotPersonIdSequence:
        """
        人物検出結果の正解ラベルの種類を検索する
        :return DomainPersonSnapshotPersonIdSequence: 人物検出結果の正解ラベルの種類リスト
        :raises NotFoundError: 人物検出結果の正解ラベルの種類が見つからない場合
        """
        with self.database as session:
            session_query = session.query(MigrationModelPersonSnapshotsAnswerLabels)
            session_query = session_query.filter(MigrationModelPersonSnapshotsAnswerLabels.is_junk.is_(False))
            session_query = session_query.distinct(MigrationModelPersonSnapshotsAnswerLabels.person_id)
            models = session_query.all()
            return DomainPersonSnapshotPersonIdSequence(items=[
                DomainPersonSnapshotPersonId(
                    id=DomainId(id=model.person_snapshot_id),
                    person_id=DomainPersonId(
                        id=DomainId(id=model.person_id) if model.person_id is not None else None,
                        is_junk=model.is_junk,
                    ),
                ) for model in models])

    def save_feature(self, person_snapshot: DomainPersonSnapshotFeature) -> None:
        with self.database as session:
            session.add(MigrationModelPersonSnapshot(
                id=person_snapshot.id.id,
                camera_id=person_snapshot.location.camera_id,
                view_id=person_snapshot.location.view_id,
                timestamp=person_snapshot.timestamp.timestamp,
                is_junk=person_snapshot.person_id.is_junk,
                person_id=person_snapshot.person_id.id.id if person_snapshot.person_id.id is not None else None,
                feature=person_snapshot.feature.value.cpu().numpy().tolist(),
            ))

    def assign_new_person_id(self, person_snapshot_ids: DomainIdSequence) -> DomainId:
        """
        人物検出結果に新しい人物IDを割り当てる
        :param DomainIdSequence person_snapshot_ids: 人物検出結果IDリスト
        :return DomainId: 新しく生成された人物ID
        :raises NotFoundError: 指定されたperson_snapshot_idが存在しない場合
        """
        with self.database as session:
            # person_snapshot_idsのリストをPythonのUUIDリストに変換
            snapshot_id_list = [snapshot_id.id for snapshot_id in person_snapshot_ids.items]
            
            # person_snapshot_idsが実際に存在するか検証
            existing_snapshots = session.query(MigrationModelPersonSnapshot).filter(
                MigrationModelPersonSnapshot.id.in_(snapshot_id_list)
            ).all()
            
            existing_snapshot_ids = {snapshot.id for snapshot in existing_snapshots}
            missing_ids = [sid for sid in snapshot_id_list if sid not in existing_snapshot_ids]
            
            if missing_ids:
                raise NotFoundError(f"指定された人物検出結果が見つかりません: {missing_ids}")
            
            # 新しい人物IDを生成
            new_person_id = uuid.uuid4()
            
            # 既存のラベルを取得
            existing_labels = session.query(MigrationModelPersonSnapshotsAnswerLabels).filter(
                MigrationModelPersonSnapshotsAnswerLabels.person_snapshot_id.in_(snapshot_id_list)
            ).all()
            
            existing_label_dict = {label.person_snapshot_id: label for label in existing_labels}
            
            # すべてのスナップショットに新しいperson_idを割り当て
            for snapshot_id in person_snapshot_ids.items:
                if snapshot_id.id in existing_label_dict:
                    # 既存のラベルを更新
                    existing_label_dict[snapshot_id.id].person_id = new_person_id
                    existing_label_dict[snapshot_id.id].is_junk = False
                else:
                    # 新しいラベルを作成
                    session.add(MigrationModelPersonSnapshotsAnswerLabels(
                        person_snapshot_id=snapshot_id.id,
                        person_id=new_person_id,
                        is_junk=False,
                    ))
            
            return DomainId(id=new_person_id)

