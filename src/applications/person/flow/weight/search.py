"""
人物フロー重み検索アプリケーション

時刻範囲で人物検出結果を取得し、フローからカメラ間の重みを算出して返す。
"""
from repositories.person.snapshot import RepositoryPersonSnapshot
from repositories.utils.database.query.person_snapshot import RepositoryUtilDatabaseQueryPersonSnapshot
from environment import Environment
from applications import ApplicationBase
from dto.person.flow.weight.query import DtoPersonFlowWeightQuery
from dto.person.flow.weight import DtoPersonFlowWeight


class ApplicationPersonFlowWeightSearch(ApplicationBase):
    """
    人物フロー重みを検索するアプリケーションクラス。
    """

    def __init__(self, repository_person_snapshot: RepositoryPersonSnapshot):
        """
        アプリケーションを初期化する。

        :param RepositoryPersonSnapshot repository_person_snapshot: 人物検出結果リポジトリ
        """
        self.repository_person_snapshot = repository_person_snapshot

    @classmethod
    def create(cls, environment: Environment) -> "ApplicationPersonFlowWeightSearch":
        """
        環境からアプリケーションインスタンスを生成する。

        :param Environment environment: 環境設定
        :return ApplicationPersonFlowWeightSearch: アプリケーションインスタンス
        """
        return cls(
            repository_person_snapshot=RepositoryPersonSnapshot.create(
                environment=environment),
        )

    def search(self, query: DtoPersonFlowWeightQuery | None = None) -> list[DtoPersonFlowWeight]:
        """
        人流の重みを検索する
        :param DtoPersonFlowWeightQuery query: 人流の重み検索条件
        :return list[DtoPersonFlowWeight]: 人流の重みリスト
        :raises ApplicationPersonFlowWeightSearchError: 人流の重み検索に失敗した場合に発生するエラー
        """
        filters = None
        if query is not None:
            filters = RepositoryUtilDatabaseQueryPersonSnapshot(
                timestamp_after=query.timestamp_after,
                timestamp_before=query.timestamp_before,
            )
        person_snapshots = self.repository_person_snapshot.find_details(
            query=filters)
        flows = person_snapshots.to_flows()
        weights = flows.to_weights()
        return [DtoPersonFlowWeight(
            source_camera_id=weight.source_location.camera_id,
            target_camera_id=weight.target_location.camera_id,
            weight=weight.weight,
        ) for weight in weights]
