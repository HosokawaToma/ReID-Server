"""
人物検出ジャンク判定のバックグラウンドプレゼンテーション層

1回の handle でジャンク判定を1件実行し、ログに記録する。
"""
from background.presentations.utils import BackgroundPresentationUtilsBase
from background.applications.person.snapshot.detect_junk import BackgroundApplicationPersonSnapshotDetectJunk
from environment import Environment
from logger import Logger


class BackgroundPersonSnapshotDetectJunk(BackgroundPresentationUtilsBase):
    """
    人物検出ジャンク判定のバックグラウンドタスクを担当するプレゼンテーション。

    キューから1件取り出してジャンク判定を1件実行し、処理結果をログに記録する。
    """

    def __init__(
        self,
        logger: Logger,
        application: BackgroundApplicationPersonSnapshotDetectJunk,
    ):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        :param BackgroundApplicationPersonSnapshotDetectJunk application: ジャンク判定アプリケーション
        """
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotDetectJunk":
        """
        環境からプレゼンテーションインスタンスを生成する。

        :param Environment environment: 環境設定
        :return BackgroundPersonSnapshotDetectJunk: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("background_person_snapshot_detect_junk"),
            application=BackgroundApplicationPersonSnapshotDetectJunk.create(
                environment),
        )

    @property
    def name(self) -> str:
        """タスク名を返す。"""
        return "person_snapshot_detect_junk"

    def handle(self, process_id: str) -> None:
        """
        ジャンク判定を1件実行し、処理したIDをログに出力する。

        :param str process_id: プロセスID（ログ用）
        """
        id = self.application.detect_junk()
        self.logger.background_info(
            process_id=process_id,
            name=self.name,
            message=f"person snapshot detect junk: {id.id}",
        )
