from repositories.utils.database import RepositoryUtilDatabase
from repositories.utils.base import RepositoryUtilBase
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
from domain.paging import DomainPaging
import torch

class RepositoryPersonSnapshot(RepositoryUtilBase):
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

    def find_ids_by_ids(self, ids: DomainIdSequence) -> DomainIdSequence:
        """
        指定されたIDリストに対応する人物検出結果のIDを取得する
        :param DomainIdSequence ids: 検索するIDリスト
        :return DomainIdSequence: 見つかったIDリスト
        :raises NotFoundError: 指定されたIDが存在しない場合
        """
        with self.database as session:
            id_list = [id_item.id for id_item in ids.items]
            models = session.query(MigrationModelPersonSnapshot).filter(
                MigrationModelPersonSnapshot.id.in_(id_list)
            ).all()
            found_ids = {model.id for model in models}
            missing_ids = [id_val for id_val in id_list if id_val not in found_ids]
            if missing_ids:
                raise NotFoundError(f"person_snapshot not found: {missing_ids}")
            return DomainIdSequence(items=[DomainId(id=model.id) for model in models])

    def count(self, query: RepositoryUtilDatabaseQueryPersonSnapshot | None = None) -> int:
        """
        人物検出結果の数を取得する
        :param RepositoryUtilDatabaseQueryPersonSnapshot query: クエリ
        :return int: 人物検出結果の数
        :raises NotFoundError: 人物検出結果が見つからない場合
        """
        with self.database as session:
            session_query = session.query(MigrationModelPersonSnapshot)
            if query is not None:
                session_query = query.build(session_query)
            return session_query.count()

    def count_by_ranking(self, person_snapshot: DomainPersonSnapshotDetail) -> int:
        """
        人物検出結果のランキングの数を取得する
        :param DomainPersonSnapshotDetail person_snapshot: 人物検出結果
        :return int: 人物検出結果のランキングの数
        :raises NotFoundError: 人物検出結果のランキングが見つからない場合
        """
        with self.database as session:
            query = session.query(MigrationModelPersonSnapshot).filter(MigrationModelPersonSnapshot.id != person_snapshot.id.id)
            query = query.filter(MigrationModelPersonSnapshot.camera_id != person_snapshot.location.camera_id)
            query = query.filter(MigrationModelPersonSnapshot.is_junk.is_(False))
            query = query.filter(MigrationModelPersonSnapshot.timestamp < person_snapshot.timestamp.tomorrow().timestamp)
            query = query.filter(MigrationModelPersonSnapshot.timestamp >= person_snapshot.timestamp.today().timestamp)
            return query.count()

    def count_by_nearest(self, person_snapshot: DomainPersonSnapshotDetail) -> int:
        """
        同じ日付で特徴量が最も近い順に人物検出結果の数を取得する
        :param DomainPersonSnapshotDetail person_snapshot: 人物検出結果
        :return int: 人物検出結果の数
        :raises NotFoundError: 人物検出結果の特徴量が見つからない場合
        """
        with self.database as session:
            query = session.query(MigrationModelPersonSnapshot).filter(MigrationModelPersonSnapshot.id != person_snapshot.id.id)
            query = query.filter(MigrationModelPersonSnapshot.timestamp < person_snapshot.timestamp.tomorrow().timestamp)
            query = query.filter(MigrationModelPersonSnapshot.timestamp >= person_snapshot.timestamp.today().timestamp)
            return query.count()

    def find_detail_by_id(self, person_snapshot_id: DomainId) -> DomainPersonSnapshotDetail:
        """
        人物検出結果の詳細を取得する
        :param DomainId person_snapshot_id: 人物検出結果のID
        :return DomainPersonSnapshotDetail: 人物検出結果の詳細
        :raises NotFoundError: 人物検出結果の詳細が見つからない場合
        """
        with self.database as session:
            model = session.query(MigrationModelPersonSnapshot).filter(MigrationModelPersonSnapshot.id == person_snapshot_id.id).first()
            if model is None:
                raise NotFoundError("人物検出結果が見つかりません")
            return DomainPersonSnapshotDetail(
                id=DomainId(id=model.id),
                location=DomainLocation(camera_id=model.camera_id, view_id=model.view_id),
                timestamp=DomainTimestamp(timestamp=model.timestamp),
                person_id=DomainPersonId(id=DomainId(id=model.person_id) if model.person_id is not None else None),
            )

    def search_details(
        self,
        paging: DomainPaging,
        query: RepositoryUtilDatabaseQueryPersonSnapshot | None = None,
    ) -> DomainPersonSnapshotDetailSequence:
        """
        人物検出結果を検索する
        :param DomainPaging paging: ページング
        :param RepositoryUtilDatabaseQueryPersonSnapshot query: クエリ
        :return DomainPersonSnapshotDetailSequence: 人物検出結果リスト
        :raises NotFoundError: 人物検出結果が見つからない場合
        """
        with self.database as session:
            session_query = session.query(MigrationModelPersonSnapshot)
            if query is not None:
                session_query = query.build(session_query)
            session_query = self._apply_paging(session_query, paging)
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

    def search_details_by_ranking(
        self,
        person_snapshot: DomainPersonSnapshotFeature,
        paging: DomainPaging,
    ) -> DomainPersonSnapshotDetailSequence:
        """
        別カメラの同じ日に検出されたゴミデータではない人物検出結果を特徴量が最も近い順に検索する
        ※同じ検出結果は除外する
        :param DomainPersonSnapshotFeature person_snapshot: 人物検出結果
        :param DomainPaging paging: ページング
        :return DomainPersonSnapshotDetailSequence: 特徴量が最も近い順に検索した人物検出結果リスト
        """
        with self.database as session:
            query = session.query(MigrationModelPersonSnapshot)
            query = query.filter(MigrationModelPersonSnapshot.id != person_snapshot.id.id)
            query = query.filter(MigrationModelPersonSnapshot.camera_id != person_snapshot.location.camera_id)
            query = query.filter(MigrationModelPersonSnapshot.is_junk.is_(False))
            query = query.filter(MigrationModelPersonSnapshot.timestamp < person_snapshot.timestamp.tomorrow().timestamp)
            query = query.filter(MigrationModelPersonSnapshot.timestamp >= person_snapshot.timestamp.today().timestamp)
            query = query.order_by(MigrationModelPersonSnapshot.feature.op("<=>")(person_snapshot.feature._feature.cpu().numpy().tolist()))
            query = self._apply_paging(query, paging)
            models = query.all()
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

    def search_details_by_nearest(self, person_snapshot: DomainPersonSnapshotFeature, paging: DomainPaging) -> DomainPersonSnapshotDetailSequence:
        """
        同じ日付で特徴量が最も近い順に人物検出結果を検索する
        :param DomainPersonSnapshotFeature person_snapshot: 人物検出結果
        :param DomainPaging paging: ページング
        :return DomainPersonSnapshotDetailSequence: 特徴量が最も近い順に検索した人物検出結果リスト
        """
        with self.database as session:
            query = session.query(MigrationModelPersonSnapshot)
            query = query.filter(MigrationModelPersonSnapshot.id != person_snapshot.id.id)
            query = query.filter(MigrationModelPersonSnapshot.timestamp < person_snapshot.timestamp.tomorrow().timestamp)
            query = query.filter(MigrationModelPersonSnapshot.timestamp >= person_snapshot.timestamp.today().timestamp)
            query = query.order_by(MigrationModelPersonSnapshot.feature.op("<=>")(person_snapshot.feature._feature.cpu().numpy().tolist()))
            query = self._apply_paging(query, paging)
            models = query.all()
            return DomainPersonSnapshotDetailSequence(items=[
                DomainPersonSnapshotDetail(
                    id=DomainId(id=model.id),
                    location=DomainLocation(camera_id=model.camera_id, view_id=model.view_id),
                    timestamp=DomainTimestamp(timestamp=model.timestamp),
                    person_id=DomainPersonId(id=DomainId(id=model.person_id) if model.person_id is not None else None, is_junk=model.is_junk),
                ) for model in models])

    def find_feature_by_id(self, person_snapshot_id: DomainId) -> DomainPersonSnapshotFeature:
        """
        人物検出結果の特徴量を取得します
        :param DomainId person_snapshot_id: 人物検出結果のID
        :return DomainPersonSnapshotFeature: 人物検出結果の特徴量
        :raise NotFoundError: 人物検出結果が見つからない場合
        :raise NotFoundError: 人物検出結果の特徴量が存在しない場合
        """
        with self.database as session:
            model = session.query(MigrationModelPersonSnapshot).filter(MigrationModelPersonSnapshot.id == person_snapshot_id.id).first()
            if model is None:
                raise NotFoundError("人物検出結果が見つかりません")
            if model.feature is None:
                raise NotFoundError("人物検出結果の特徴量が存在しません")
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
            query = query.filter(MigrationModelPersonSnapshot.id != person_snapshot.id.id)
            query = query.filter(MigrationModelPersonSnapshot.timestamp <= person_snapshot.timestamp.timestamp)
            query = query.filter(MigrationModelPersonSnapshot.timestamp >= person_snapshot.timestamp.today().timestamp)
            query = query.filter(MigrationModelPersonSnapshot.is_junk.is_(False))
            query = query.filter(MigrationModelPersonSnapshot.feature.isnot(None))
            query = query.order_by(MigrationModelPersonSnapshot.feature.op("<=>")(person_snapshot.feature._feature.cpu().numpy().tolist()))
            model = query.first()
            if model is None:
                raise NotFoundError("特徴量が最も近い人物検出結果が見つかりません")
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

    def find_answer_label_by_id(self, person_snapshot_id: DomainId) -> DomainPersonSnapshotPersonId:
        """
        人物検出結果の正解ラベルを取得する
        :param DomainId person_snapshot_id: 人物検出結果のID
        :return DomainPersonSnapshotPersonId: 人物検出結果の正解ラベル
        :raises NotFoundError: 人物検出結果の正解ラベルが見つからない場合
        """
        with self.database as session:
            model = session.query(MigrationModelPersonSnapshotsAnswerLabels).filter(MigrationModelPersonSnapshotsAnswerLabels.person_snapshot_id == person_snapshot_id.id).first()
            if model is None:
                raise NotFoundError("人物検出結果の正解ラベルが見つかりません")
            return DomainPersonSnapshotPersonId(
                id=DomainId(id=model.person_snapshot_id),
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

    def add_answer_label(self, person_snapshot_person_id: DomainPersonSnapshotPersonId) -> None:
        """
        人物検出結果の正解ラベルを追加する
        :param DomainPersonSnapshotPersonId person_snapshot_person_id: 人物検出結果の正解ラベル
        """
        with self.database as session:
            session.add(MigrationModelPersonSnapshotsAnswerLabels(
                person_snapshot_id=person_snapshot_person_id.id.id,
                person_id=person_snapshot_person_id.person_id.id.id if person_snapshot_person_id.person_id.id is not None else None,
                is_junk=person_snapshot_person_id.person_id.is_junk,
            ))

    def save_answer_labels(self, person_snapshot_person_ids: DomainPersonSnapshotPersonIdSequence) -> None:
        """
        人物検出結果の正解ラベルを保存する
        :param DomainPersonSnapshotPersonIdSequence person_snapshot_person_ids: 人物検出結果の正解ラベルリスト
        """
        with self.database as session:
            for item in person_snapshot_person_ids.items:
                session.merge(MigrationModelPersonSnapshotsAnswerLabels(
                    person_snapshot_id=item.id.id,
                    person_id=item.person_id.id.id if item.person_id.id is not None else None,
                    is_junk=item.person_id.is_junk,
                ))

    def save_feature(self, person_snapshot: DomainPersonSnapshotFeature) -> None:
        """
        人物検出結果の特徴量を保存する
        既存レコードがある場合は更新し、ない場合は追加する
        :param DomainPersonSnapshotFeature person_snapshot: 人物検出結果の特徴量
        """
        with self.database as session:
            session.merge(MigrationModelPersonSnapshot(
                id=person_snapshot.id.id,
                camera_id=person_snapshot.location.camera_id,
                view_id=person_snapshot.location.view_id,
                timestamp=person_snapshot.timestamp.timestamp,
                is_junk=person_snapshot.person_id.is_junk,
                person_id=person_snapshot.person_id.id.id if person_snapshot.person_id.id is not None else None,
                feature=person_snapshot.feature._feature.cpu().numpy().tolist(),
            ))

    def update_answer_labels(self, person_snapshot_person_ids: DomainPersonSnapshotPersonIdSequence) -> None:
        """
        人物検出結果の正解ラベルを更新する
        :param DomainPersonSnapshotPersonIdSequence person_snapshot_person_ids: 人物検出結果の人物IDリスト
        """
        with self.database as session:
            for item in person_snapshot_person_ids.items:
                session.merge(MigrationModelPersonSnapshotsAnswerLabels(
                    person_snapshot_id=item.id.id,
                    person_id=item.person_id.id.id if item.person_id.id is not None else None,
                    is_junk=item.person_id.is_junk,
                ))

    def delete_answer_label_by_id(self, person_snapshot_id: DomainId) -> None:
        """
        人物検出結果の正解ラベルを削除する
        :param DomainId person_snapshot_id: 人物検出結果のID
        """
        with self.database as session:
            query = session.query(MigrationModelPersonSnapshotsAnswerLabels)
            query = query.filter(MigrationModelPersonSnapshotsAnswerLabels.person_snapshot_id == person_snapshot_id.id)
            query.delete()
