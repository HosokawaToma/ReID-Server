"""
人物検出特徴量抽出のバックグラウンドプレゼンテーション層

1回の handle で特徴量抽出を1件実行し、処理したIDをログに記録する。
"""
from background.presentations.utils import BackgroundPresentationUtilsBase
from background.applications.person.snapshot.feature_extract import BackgroundApplicationPersonSnapshotFeatureExtract
from environment import Environment
from logger import Logger


class BackgroundPersonSnapshotFeatureExtract(BackgroundPresentationUtilsBase):
    """
    人物検出特徴量抽出のバックグラウンドタスクを担当するプレゼンテーション。

    キューから1件取り出して特徴量抽出を1件実行し、処理したIDをログに記録する。
    """

    def __init__(
        self,
        logger: Logger,
        application: BackgroundApplicationPersonSnapshotFeatureExtract,
    ):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        :param BackgroundApplicationPersonSnapshotFeatureExtract application: 特徴量抽出アプリケーション
        """
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotFeatureExtract":
        """
        環境変数からプレゼンテーションインスタンスを生成する。

        :param Environment environment: 環境変数
        :return BackgroundPersonSnapshotFeatureExtract: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("background_person_snapshot_feature_extract"),
            application=BackgroundApplicationPersonSnapshotFeatureExtract.create(
                environment),
        )

    @property
    def name(self) -> str:
        """タスク名を返す。"""
        return "person_snapshot_feature_extract"

    def handle(self, process_id: str) -> None:
        """
        特徴量抽出を1件実行し、処理したIDをログに出力する。

        :param str process_id: プロセスID（ログ用）
        """
        id = self.application.extract()
        self.logger.background_info(
            process_id=process_id,
            name=self.name,
            message=f"person snapshot feature extracted: {id.id}",
        )
