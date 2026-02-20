"""
バックグラウンドプロセスエントリポイント

人物検出作成・再識別・特徴量抽出・ジャンク判定の各タスクを非同期で起動・停止する。
"""
from environment import Environment
from background.presentations.person.snapshot.create import BackgroundPersonSnapshotCreate
from background.presentations.person.snapshot.reid import BackgroundPersonSnapshotReid
from background.presentations.person.snapshot.feature_extract import BackgroundPersonSnapshotFeatureExtract
from background.presentations.person.snapshot.detect_junk import BackgroundPersonSnapshotDetectJunk
import asyncio
import signal


class BackgroundMain:
    """
    バックグラウンドタスクの統合。

    人物検出作成・再識別・特徴量抽出・ジャンク判定の各タスクを保持し、一括で起動・停止できる。
    """

    def __init__(
        self,
        person_snapshot_create: BackgroundPersonSnapshotCreate,
        person_snapshot_reid: BackgroundPersonSnapshotReid,
        person_snapshot_feature_extract: BackgroundPersonSnapshotFeatureExtract,
        person_snapshot_detect_junk: BackgroundPersonSnapshotDetectJunk,
    ):
        """
        バックグラウンドメインを初期化する。

        :param BackgroundPersonSnapshotCreate person_snapshot_create: 人物検出作成タスク
        :param BackgroundPersonSnapshotReid person_snapshot_reid: 再識別タスク
        :param BackgroundPersonSnapshotFeatureExtract person_snapshot_feature_extract: 特徴量抽出タスク
        :param BackgroundPersonSnapshotDetectJunk person_snapshot_detect_junk: ジャンク判定タスク
        """
        self.person_snapshot_create = person_snapshot_create
        self.person_snapshot_reid = person_snapshot_reid
        self.person_snapshot_feature_extract = person_snapshot_feature_extract
        self.person_snapshot_detect_junk = person_snapshot_detect_junk

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundMain":
        """
        環境変数からバックグラウンドメインインスタンスを生成する。

        :param Environment environment: 環境変数
        :return BackgroundMain: バックグラウンドメインインスタンス
        """
        return cls(
            person_snapshot_create=BackgroundPersonSnapshotCreate.create(
                environment=environment),
            person_snapshot_reid=BackgroundPersonSnapshotReid.create(
                environment=environment),
            person_snapshot_feature_extract=BackgroundPersonSnapshotFeatureExtract.create(
                environment=environment),
            person_snapshot_detect_junk=BackgroundPersonSnapshotDetectJunk.create(
                environment=environment),
        )

    async def run(self) -> None:
        """
        SIGINT/SIGTERMで停止するまで、各タスクを起動したうえでイベント待ちする。
        """
        event = asyncio.Event()
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, event.set)
        loop.add_signal_handler(signal.SIGTERM, event.set)
        try:
            await self.start()
            await event.wait()
        finally:
            await self.stop()

    async def start(self) -> None:
        """
        各バックグラウンドタスクを起動する。
        """
        await self.person_snapshot_create.start()
        await self.person_snapshot_reid.start()
        await self.person_snapshot_feature_extract.start()
        await self.person_snapshot_detect_junk.start()

    async def stop(self) -> None:
        """
        各バックグラウンドタスクを停止する。
        """
        await self.person_snapshot_create.stop()
        await self.person_snapshot_reid.stop()
        await self.person_snapshot_feature_extract.stop()
        await self.person_snapshot_detect_junk.stop()


if __name__ == "__main__":
    background_main = BackgroundMain.create(environment=Environment())
    asyncio.run(background_main.run())
