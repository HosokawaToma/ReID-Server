from repositories.utils.database import RepositoryUtilDatabase
from error import NotFoundError
from environment import Environment
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshot
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

    def find_answer_label_kinds(self) -> DomainPersonSnapshotPersonIdSequence:
        with self.database as session:
            session_query = session.query(MigrationModelPersonSnapshotsAnswerLabels)
            session_query = session_query.filter(MigrationModelPersonSnapshotsAnswerLabels.is_junk.is_(False))
            session_query = session_query.distinct(MigrationModelPersonSnapshotsAnswerLabels.person_id)
            session_query = session_query.order_by(MigrationModelPersonSnapshotsAnswerLabels.created_at.desc())
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
