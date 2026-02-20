"""
人物検出再同定のバックグラウンドプレゼンテーション層

1回の handle で再同定を1件実行し、処理したIDをログに記録する。
"""
from background.presentations.utils import BackgroundPresentationUtilsBase
from background.applications.person.snapshot.reid import BackgroundApplicationPersonSnapshotReid
from environment import Environment
from logger import Logger


class BackgroundPersonSnapshotReid(BackgroundPresentationUtilsBase):
    """
    人物検出再同定のバックグラウンドタスクを担当するプレゼンテーション。

    キューから1件取り出して再同定を1件実行し、処理したIDをログに記録する。
    """

    def __init__(
        self,
        logger: Logger,
        application: BackgroundApplicationPersonSnapshotReid,
    ):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        :param BackgroundApplicationPersonSnapshotReid application: 再同定アプリケーション
        """
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotReid":
        """
        環境変数からプレゼンテーションインスタンスを生成する。

        :param Environment environment: 環境変数
        :return BackgroundPersonSnapshotReid: プレゼンテーションインスタンス
        """
        return cls(
            application=BackgroundApplicationPersonSnapshotReid.create(
                environment),
            logger=Logger("background_person_snapshot_reid"),
        )

    @property
    def name(self) -> str:
        """タスク名を返す。"""
        return "person_snapshot_reid"

    def handle(self, process_id: str) -> None:
        """
        再同定を1件実行し、処理した人物検出IDをログに出力する。

        :param str process_id: プロセスID（ログ用）
        """
        person_snapshot_person_id = self.application.reid()
        self.logger.background_info(
            process_id=process_id,
            name=self.name,
            message=f"person snapshot id: {person_snapshot_person_id.id} reid",
        )
