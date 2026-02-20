"""
人物検出作成のバックグラウンドプレゼンテーション層

1回の handle で人物検出を1件作成し、作成件数をログに記録する。
"""
from background.presentations.utils import BackgroundPresentationUtilsBase
from logger import Logger
from background.applications.person.snapshot.create import BackgroundApplicationPersonSnapshotCreate
from environment import Environment


class BackgroundPersonSnapshotCreate(BackgroundPresentationUtilsBase):
    """
    人物検出作成のバックグラウンドタスクを担当するプレゼンテーション。

    キューから1件取り出して人物検出を1件作成し、作成件数をログに記録する。
    """

    def __init__(
        self,
        logger: Logger,
        application: BackgroundApplicationPersonSnapshotCreate,
    ):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        :param BackgroundApplicationPersonSnapshotCreate application: 人物検出作成アプリケーション
        """
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotCreate":
        """
        環境からプレゼンテーションインスタンスを生成する。

        :param Environment environment: 環境設定
        :return BackgroundPersonSnapshotCreate: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("background_person_snapshot_create"),
            application=BackgroundApplicationPersonSnapshotCreate.create(
                environment),
        )

    @property
    def name(self) -> str:
        """タスク名を返す。"""
        return "person_snapshot_create"

    def handle(self, process_id: str) -> None:
        """
        人物検出を1件作成し、作成した件数をログに出力する。

        :param str process_id: プロセスID（ログ用）
        """
        person_snapshots = self.application.save()
        self.logger.background_info(
            process_id=process_id,
            name=self.name,
            message=f"person snapshots created: {len(person_snapshots)}",
        )
