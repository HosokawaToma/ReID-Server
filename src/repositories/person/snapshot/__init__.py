from repositories.utils.database import RepositoryUtilDatabase
from repositories.utils.base import RepositoryUtilBase
from error import NotFoundError, ValidationError
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
from domain.date import DomainDate
from domain.reid.rank import DomainReidRank
from domain.reid.rank_sequence import DomainReidRankSequence
from sqlalchemy import func
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

    def find_detail_answer_by_id(self, person_snapshot_id: DomainId) -> DomainPersonSnapshotDetail:
        """
        person_idが正解データの人物検出結果の詳細を取得する
        :param DomainId person_snapshot_id: 人物検出結果のID
        :return DomainPersonSnapshotDetail: person_idが正解データの人物検出結果の詳細
        :raises NotFoundError: person_idが正解データの人物検出結果の詳細が見つからない場合
        """
        with self.database as session:
            model = session.query(
                MigrationModelPersonSnapshot, MigrationModelPersonSnapshotsAnswerLabels
            ).join(
                MigrationModelPersonSnapshotsAnswerLabels,
                MigrationModelPersonSnapshot.id == MigrationModelPersonSnapshotsAnswerLabels.person_snapshot_id
            ).filter(MigrationModelPersonSnapshot.id == person_snapshot_id.id).first()
            if model is None:
                raise NotFoundError("人物検出結果が見つかりません")
            person_snapshot, answer_label = model
            person_snapshot: MigrationModelPersonSnapshot
            answer_label: MigrationModelPersonSnapshotsAnswerLabels
            return DomainPersonSnapshotDetail(
                id=DomainId(id=person_snapshot.id),
                location=DomainLocation(camera_id=person_snapshot.camera_id, view_id=person_snapshot.view_id),
                timestamp=DomainTimestamp(timestamp=person_snapshot.timestamp),
                person_id=DomainPersonId(
                    id=DomainId(id=answer_label.person_id) if answer_label.person_id is not None else None,
                    is_junk=answer_label.is_junk,
                ),
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
        別カメラの同じ日に検出された人物検出結果を特徴量が最も近い順に検索する
        ※同じ検出結果は除外する
        :param DomainPersonSnapshotFeature person_snapshot: 人物検出結果
        :param DomainPaging paging: ページング
        :return DomainPersonSnapshotDetailSequence: 特徴量が最も近い順に検索した人物検出結果リスト
        """
        with self.database as session:
            query = session.query(MigrationModelPersonSnapshot)
            query = query.filter(MigrationModelPersonSnapshot.id != person_snapshot.id.id)
            query = query.filter(MigrationModelPersonSnapshot.camera_id != person_snapshot.location.camera_id)
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

    def search_query_is_junk(self, date: DomainDate, paging: DomainPaging) -> DomainIdSequence:
        """
        特定日のクエリデータを取得する
        ※同じ人物IDは1件しか取得しない
        :param DomainDate date: 日付
        :param DomainPaging paging: ページング
        :return DomainIdSequence: クエリデータIDリスト
        :raises NotFoundError: クエリデータが見つからない場合
        """
        with self.database as session:
            query = session.query(
                MigrationModelPersonSnapshot,
                MigrationModelPersonSnapshotsAnswerLabels
            ).join(
                MigrationModelPersonSnapshotsAnswerLabels,
                MigrationModelPersonSnapshot.id == MigrationModelPersonSnapshotsAnswerLabels.person_snapshot_id
            ).filter(
                MigrationModelPersonSnapshot.timestamp >= DomainTimestamp.from_date(date).today().timestamp
            ).filter(
                MigrationModelPersonSnapshot.timestamp < DomainTimestamp.from_date(date).tomorrow().timestamp
            ).filter(
                MigrationModelPersonSnapshot.is_junk.is_(True)
            ).distinct(
                MigrationModelPersonSnapshotsAnswerLabels.person_id
            ).order_by(
                MigrationModelPersonSnapshotsAnswerLabels.person_id,
                func.random()
            )
            query = self._apply_paging(query, paging)
            models = query.all()
            items: list[DomainId] = []
            for snapshot, _ in models:
                snapshot: MigrationModelPersonSnapshot
                items.append(DomainId(id=snapshot.id))
            return DomainIdSequence(items=items)

    def count_query_is_junk(self, date: DomainDate) -> int:
        """
        特定日のクエリデータの数を取得する
        :param DomainDate date: 日付
        :return int: クエリデータの数
        :raises NotFoundError: クエリデータが見つからない場合
        """
        with self.database as session:
            return session.query(MigrationModelPersonSnapshot, MigrationModelPersonSnapshotsAnswerLabels).join(
                MigrationModelPersonSnapshotsAnswerLabels,
                MigrationModelPersonSnapshot.id == MigrationModelPersonSnapshotsAnswerLabels.person_snapshot_id
            ).filter(
                MigrationModelPersonSnapshot.timestamp >= DomainTimestamp.from_date(date).today().timestamp
            ).filter(
                MigrationModelPersonSnapshot.timestamp < DomainTimestamp.from_date(date).tomorrow().timestamp
            ).filter(
                MigrationModelPersonSnapshot.is_junk.is_(True)
            ).distinct(
                MigrationModelPersonSnapshotsAnswerLabels.person_id
            ).count()

    def search_query_is_not_junk(self, date: DomainDate, paging: DomainPaging) -> DomainIdSequence:
        """
        特定日のクエリデータを取得する
        ※ゴミデータは除外する
        :param DomainDate date: 日付
        :param DomainPaging paging: ページング
        :return DomainIdSequence: クエリデータIDリスト
        :raises NotFoundError: クエリデータが見つからない場合
        """
        with self.database as session:
            query = session.query(
                MigrationModelPersonSnapshot, MigrationModelPersonSnapshotsAnswerLabels
            ).join(
                MigrationModelPersonSnapshotsAnswerLabels,
                MigrationModelPersonSnapshot.id == MigrationModelPersonSnapshotsAnswerLabels.person_snapshot_id
            ).filter(
                MigrationModelPersonSnapshot.timestamp >= DomainTimestamp.from_date(date).today().timestamp
            ).filter(
                MigrationModelPersonSnapshot.timestamp < DomainTimestamp.from_date(date).tomorrow().timestamp
            ).filter(
                MigrationModelPersonSnapshot.is_junk.is_(False)
            ).distinct(
                MigrationModelPersonSnapshotsAnswerLabels.person_id
            ).order_by(
                MigrationModelPersonSnapshotsAnswerLabels.person_id,
                func.random()
            )
            query = self._apply_paging(query, paging)
            models = query.all()
            items: list[DomainId] = []
            for snapshot, _ in models:
                snapshot: MigrationModelPersonSnapshot
                items.append(DomainId(id=snapshot.id))
            return DomainIdSequence(items=items)

    def count_query_is_not_junk(self, date: DomainDate) -> int:
        """
        特定日のクエリデータの数を取得する
        :param DomainDate date: 日付
        :return int: クエリデータの数
        :raises NotFoundError: クエリデータが見つからない場合
        """
        with self.database as session:
            return session.query(
                MigrationModelPersonSnapshot, MigrationModelPersonSnapshotsAnswerLabels
                ).join(
                    MigrationModelPersonSnapshotsAnswerLabels,
                    MigrationModelPersonSnapshot.id == MigrationModelPersonSnapshotsAnswerLabels.person_snapshot_id
                ).filter(
                    MigrationModelPersonSnapshot.timestamp >= DomainTimestamp.from_date(date).today().timestamp
                ).filter(
                    MigrationModelPersonSnapshot.timestamp <= DomainTimestamp.from_date(date).tomorrow().timestamp
                ).filter(
                    MigrationModelPersonSnapshot.is_junk.is_(False)
                ).distinct(
                    MigrationModelPersonSnapshotsAnswerLabels.person_id
                ).count()

    def search_gallery_contains_junk(self, person_snapshot_feature: DomainPersonSnapshotFeature) -> DomainIdSequence:
        """
        ギャラリーデータを特徴量が最も近い順に取得する
        ※ゴミデータを含む
        ギャラリーデータとは同じ日付で別カメラで同じIDの人物検出結果を除外したもの
        :param DomainPersonSnapshotFeature person_snapshot_feature: 人物検出結果の特徴量
        :return DomainIdSequence: ギャラリーIDリスト
        """
        with self.database as session:
            models = session.query(
                MigrationModelPersonSnapshot
            ).filter(
                MigrationModelPersonSnapshot.id != person_snapshot_feature.id.id
            ).filter(
                MigrationModelPersonSnapshot.camera_id != person_snapshot_feature.location.camera_id
            ).filter(
                MigrationModelPersonSnapshot.timestamp < person_snapshot_feature.timestamp.tomorrow().timestamp
            ).filter(
                MigrationModelPersonSnapshot.timestamp >= person_snapshot_feature.timestamp.today().timestamp
            ).order_by(
                MigrationModelPersonSnapshot.feature.op("<=>")(person_snapshot_feature.feature._feature.cpu().numpy().tolist())
            ).limit(50).all()
            return DomainIdSequence(
                items=[DomainId(id=model.id) for model in models]
            )

    def exists_gallery_contains_junk(self, person_snapshot_detail_answer: DomainPersonSnapshotDetail) -> bool:
        """
        ギャラリーデータに正解データが含まれているかを検証する
        :param DomainPersonSnapshotDetailAnswer person_snapshot_detail_answer: person_idが正解データの人物検出結果
        :return bool: ギャラリーデータに正解データが含まれているか
        """
        if person_snapshot_detail_answer.person_id.id is None:
            raise ValidationError("検索元の人物検出結果に正解データが存在しません")
        with self.database as session:
            query = session.query(
                MigrationModelPersonSnapshot,
                MigrationModelPersonSnapshotsAnswerLabels
            ).join(
                MigrationModelPersonSnapshotsAnswerLabels,
                MigrationModelPersonSnapshot.id == MigrationModelPersonSnapshotsAnswerLabels.person_snapshot_id
            ).filter(
                MigrationModelPersonSnapshot.id != person_snapshot_detail_answer.id.id,
                MigrationModelPersonSnapshot.camera_id != person_snapshot_detail_answer.location.camera_id,
                MigrationModelPersonSnapshot.timestamp < person_snapshot_detail_answer.timestamp.tomorrow().timestamp,
                MigrationModelPersonSnapshot.timestamp >= person_snapshot_detail_answer.timestamp.today().timestamp,
                MigrationModelPersonSnapshotsAnswerLabels.person_id == person_snapshot_detail_answer.person_id.id.id,
            ).exists()
            return session.query(query).scalar()

    def search_gallery_not_contains_junk(self, person_snapshot_feature: DomainPersonSnapshotFeature) -> DomainIdSequence:
        """
        ギャラリーデータを特徴量が最も近い順に取得する
        ※ゴミデータは除外する
        ギャラリーデータとは同じ日付で別カメラで同じIDの人物検出結果を除外したもの
        :param DomainPersonSnapshotFeature person_snapshot_feature: 人物検出結果の特徴量
        :return DomainIdSequence: ギャラリーIDリスト
        """
        with self.database as session:
            models = session.query(
                MigrationModelPersonSnapshot
            ).filter(
                MigrationModelPersonSnapshot.id != person_snapshot_feature.id.id
            ).filter(
                MigrationModelPersonSnapshot.camera_id != person_snapshot_feature.location.camera_id
            ).filter(
                MigrationModelPersonSnapshot.timestamp < person_snapshot_feature.timestamp.tomorrow().timestamp
            ).filter(
                MigrationModelPersonSnapshot.timestamp >= person_snapshot_feature.timestamp.today().timestamp
            ).filter(
                MigrationModelPersonSnapshot.is_junk.is_(False)
            ).order_by(
                MigrationModelPersonSnapshot.feature.op("<=>")(person_snapshot_feature.feature._feature.cpu().numpy().tolist())
            ).limit(50).all()
            return DomainIdSequence(items=[DomainId(id=model.id) for model in models])

    def exists_gallery_not_contains_junk(self, person_snapshot_detail_answer: DomainPersonSnapshotDetail) -> bool:
        """
        ギャラリーデータに正解データが含まれていないかを検証する
        :param DomainPersonSnapshotDetailAnswer person_snapshot_detail_answer: person_idが正解データの人物検出結果
        :return bool: ギャラリーデータに正解データが含まれていないか
        """
        if person_snapshot_detail_answer.person_id.id is None:
            raise ValidationError("検索元の人物検出結果に正解データが存在しません")
        with self.database as session:
            query = session.query(
                MigrationModelPersonSnapshot, MigrationModelPersonSnapshotsAnswerLabels
            ).join(
                MigrationModelPersonSnapshotsAnswerLabels,
                MigrationModelPersonSnapshot.id == MigrationModelPersonSnapshotsAnswerLabels.person_snapshot_id
            ).filter(
                MigrationModelPersonSnapshot.id != person_snapshot_detail_answer.id.id,
                MigrationModelPersonSnapshot.camera_id != person_snapshot_detail_answer.location.camera_id,
                MigrationModelPersonSnapshot.is_junk.is_(False),
                MigrationModelPersonSnapshot.timestamp < person_snapshot_detail_answer.timestamp.tomorrow().timestamp,
                MigrationModelPersonSnapshot.timestamp >= person_snapshot_detail_answer.timestamp.today().timestamp,
                MigrationModelPersonSnapshotsAnswerLabels.person_id == person_snapshot_detail_answer.person_id.id.id,
            ).exists()
            return session.query(query).scalar()

    def find_query_is_not_junk(self, date: DomainDate, attempt: int) -> DomainIdSequence:
        """
        特定日のクエリデータを取得する
        試行回数分のクエリデータを取得する
        ※ゴミデータは除外する
        :param DomainDate date: 日付
        :param int attempt: 試行回数
        :return DomainIdSequence: クエリデータIDリスト
        """
        with self.database as session:
            subquery = session.query(
                MigrationModelPersonSnapshot.id.label("snapshot_id"),
                func.row_number().over(
                    partition_by=MigrationModelPersonSnapshotsAnswerLabels.person_id,
                    order_by=func.random()
                ).label("rn")
            ).join(
                MigrationModelPersonSnapshotsAnswerLabels,
                MigrationModelPersonSnapshot.id == MigrationModelPersonSnapshotsAnswerLabels.person_snapshot_id
            ).filter(
                MigrationModelPersonSnapshot.timestamp >= DomainTimestamp.from_date(date).today().timestamp,
                MigrationModelPersonSnapshot.timestamp < DomainTimestamp.from_date(date).tomorrow().timestamp,
                MigrationModelPersonSnapshot.is_junk.is_(False)
            ).subquery()
            query = session.query(
                subquery.c.snapshot_id
            ).filter(
                subquery.c.rn <= attempt
            )
            models = query.all()
            items: list[DomainId] = []
            for row in models:
                items.append(DomainId(id=row.snapshot_id))
            return DomainIdSequence(items=items)

    def find_gallery_not_contains_junk(self, person_snapshot_feature: DomainPersonSnapshotFeature) -> DomainIdSequence:
        """
        ギャラリーデータを取得する
        ※ゴミデータは除外する
        :param DomainPersonSnapshotFeature person_snapshot_feature: 人物検出結果の特徴量
        :return DomainIdSequence: ギャラリーIDリスト
        """
        with self.database as session:
            models = session.query(
                MigrationModelPersonSnapshot
            ).filter(
                MigrationModelPersonSnapshot.id != person_snapshot_feature.id.id,
                MigrationModelPersonSnapshot.camera_id != person_snapshot_feature.location.camera_id,
                MigrationModelPersonSnapshot.timestamp < person_snapshot_feature.timestamp.tomorrow().timestamp,
                MigrationModelPersonSnapshot.timestamp >= person_snapshot_feature.timestamp.today().timestamp,
                MigrationModelPersonSnapshot.is_junk.is_(False),
            ).order_by(
                MigrationModelPersonSnapshot.feature.op("<=>")(
                    person_snapshot_feature.feature._feature.cpu().numpy().tolist())
            ).limit(50).all()
            return DomainIdSequence(items=[DomainId(id=model.id) for model in models])

    def find_gallery_contains_junk(self, person_snapshot_feature: DomainPersonSnapshotFeature) -> DomainIdSequence:
        """
        ギャラリーデータを取得する
        ※ゴミデータを含む
        :param DomainPersonSnapshotFeature person_snapshot_feature: 人物検出結果の特徴量
        :return DomainIdSequence: ギャラリーIDリスト
        """
        with self.database as session:
            models = session.query(
                MigrationModelPersonSnapshot
            ).filter(
                MigrationModelPersonSnapshot.id != person_snapshot_feature.id.id,
                MigrationModelPersonSnapshot.camera_id != person_snapshot_feature.location.camera_id,
                MigrationModelPersonSnapshot.timestamp < person_snapshot_feature.timestamp.tomorrow().timestamp,
                MigrationModelPersonSnapshot.timestamp >= person_snapshot_feature.timestamp.today().timestamp,
            ).order_by(
                MigrationModelPersonSnapshot.feature.op("<=>")(
                    person_snapshot_feature.feature._feature.cpu().numpy().tolist())
            ).limit(50).all()
            return DomainIdSequence(items=[DomainId(id=model.id) for model in models])

    def find_answer_labels_by_ids(self, person_snapshot_ids: DomainIdSequence) -> DomainPersonSnapshotPersonIdSequence:
        """
        人物検出結果の正解ラベルを取得する
        :param DomainIdSequence person_snapshot_ids: 人物検出結果のIDリスト
        :return DomainPersonSnapshotPersonIdSequence: 人物検出結果の正解ラベルリスト
        """
        with self.database as session:
            models = session.query(
                MigrationModelPersonSnapshotsAnswerLabels
            ).filter(
                MigrationModelPersonSnapshotsAnswerLabels.person_snapshot_id.in_([person_snapshot_id.id for person_snapshot_id in person_snapshot_ids.items])
            ).all()
            return DomainPersonSnapshotPersonIdSequence(items=[DomainPersonSnapshotPersonId(
                id=DomainId(id=model.person_snapshot_id),
                person_id=DomainPersonId(
                    id=DomainId(id=model.person_id) if model.person_id is not None else None,
                    is_junk=model.is_junk,
                ),
            ) for model in models])

    def find_not_contains_junk_ranking_by_ids(self, person_snapshot_ids: DomainIdSequence, person_snapshot_feature: DomainPersonSnapshotFeature) -> DomainReidRankSequence:
        """
        人物検出結果のランキングを取得する
        ※同じカメラIDの人物検出結果は除外する
        ※ゴミデータは除外する
        :param DomainIdSequence person_snapshot_ids: 人物検出結果のIDリスト
        :param DomainPersonSnapshotFeature person_snapshot_feature: 人物検出結果の特徴量
        :return DomainReidRankSequence: 人物検出結果のランキングリスト
        """
        with self.database as session:
            subquery = session.query(
                MigrationModelPersonSnapshot.id,
                func.row_number().over(
                    order_by=MigrationModelPersonSnapshot.feature.op("<=>")(person_snapshot_feature.feature._feature.cpu().numpy().tolist())
                ).label("original_index")
            ).filter(
                MigrationModelPersonSnapshot.id != person_snapshot_feature.id.id,
                MigrationModelPersonSnapshot.camera_id != person_snapshot_feature.location.camera_id,
                MigrationModelPersonSnapshot.timestamp < person_snapshot_feature.timestamp.tomorrow().timestamp,
                MigrationModelPersonSnapshot.timestamp >= person_snapshot_feature.timestamp.today().timestamp,
                MigrationModelPersonSnapshot.is_junk.is_(False),
            ).subquery()
            models = session.query(
                subquery.c.id,
                subquery.c.original_index,
            ).filter(
                subquery.c.id.in_([person_snapshot_id.id for person_snapshot_id in person_snapshot_ids.items])
            ).all()
            return DomainReidRankSequence(items=[DomainReidRank(
                id=DomainId(id=model.id),
                rank=model.original_index,
            ) for model in models])

    def find_contains_junk_ranking_by_ids(self, person_snapshot_ids: DomainIdSequence, person_snapshot_feature: DomainPersonSnapshotFeature) -> DomainReidRankSequence:
        """
        ギャラリーデータにゴミデータを含むランキングを取得する
        :param DomainIdSequence person_snapshot_ids: 人物検出結果のIDリスト
        :param DomainPersonSnapshotFeature person_snapshot_feature: 人物検出結果の特徴量
        :return DomainReidRankSequence: ギャラリーデータにゴミデータを含むランキングリスト
        """
        with self.database as session:
            subquery = session.query(
                MigrationModelPersonSnapshot.id,
                func.row_number().over(
                    order_by=MigrationModelPersonSnapshot.feature.op("<=>")(person_snapshot_feature.feature._feature.cpu().numpy().tolist())
                ).label("original_index")
            ).filter(
                MigrationModelPersonSnapshot.id != person_snapshot_feature.id.id,
                MigrationModelPersonSnapshot.camera_id != person_snapshot_feature.location.camera_id,
                MigrationModelPersonSnapshot.timestamp < person_snapshot_feature.timestamp.tomorrow().timestamp,
                MigrationModelPersonSnapshot.timestamp >= person_snapshot_feature.timestamp.today().timestamp,
            ).subquery()
            models = session.query(
                subquery.c.id,
                subquery.c.original_index,
            ).filter(
                subquery.c.id.in_([person_snapshot_id.id for person_snapshot_id in person_snapshot_ids.items])
            ).all()
            return DomainReidRankSequence(items=[DomainReidRank(
                id=DomainId(id=model.id),
                rank=model.original_index,
            ) for model in models])

    def find_not_contains_junk_answer_labels_by_person_id(self, person_id: DomainId) -> DomainPersonSnapshotPersonIdSequence:
        """
        正解ラベルを取得する
        ※ゴミデータは除外する
        :param DomainId person_id: 人物ID
        :return DomainPersonSnapshotPersonIdSequence: 正解ラベルリスト
        """
        with self.database as session:
            models = session.query(
                MigrationModelPersonSnapshotsAnswerLabels
            ).filter(
                MigrationModelPersonSnapshotsAnswerLabels.person_id == person_id.id,
                MigrationModelPersonSnapshotsAnswerLabels.is_junk.is_(False)
            ).all()
            return DomainPersonSnapshotPersonIdSequence(items=[DomainPersonSnapshotPersonId(
                id=DomainId(id=model.person_snapshot_id),
                person_id=DomainPersonId(
                    id=DomainId(
                        id=model.person_id) if model.person_id is not None else None,
                    is_junk=model.is_junk,
                ),
            ) for model in models])

    def find_contains_junk_answer_labels_by_person_id(self, person_id: DomainId) -> DomainPersonSnapshotPersonIdSequence:
        """
        正解ラベルを取得する
        ※ゴミデータを含む
        :param DomainId person_id: 人物ID
        :return DomainPersonSnapshotPersonIdSequence: 正解ラベルリスト
        """
        with self.database as session:
            models = session.query(
                MigrationModelPersonSnapshotsAnswerLabels
            ).filter(
                MigrationModelPersonSnapshotsAnswerLabels.person_id == person_id.id
            ).all()
            return DomainPersonSnapshotPersonIdSequence(items=[DomainPersonSnapshotPersonId(
                id=DomainId(id=model.person_snapshot_id),
                person_id=DomainPersonId(
                    id=DomainId(id=model.person_id) if model.person_id is not None else None,
                    is_junk=model.is_junk,
                ),
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

    def save_person_id(self, person_snapshot_person_id: DomainPersonSnapshotPersonId) -> None:
        """
        人物検出結果の人物IDを保存する
        :param DomainPersonSnapshotPersonId person_snapshot_person_id: 人物検出結果の人物ID
        """
        with self.database as session:
            session.merge(MigrationModelPersonSnapshot(
                id=person_snapshot_person_id.id.id,
                person_id=person_snapshot_person_id.person_id.id.id if person_snapshot_person_id.person_id.id is not None else None,
                is_junk=person_snapshot_person_id.person_id.is_junk,
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
