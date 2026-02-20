"""
バックグラウンドプレゼンテーション基底

非同期でループ実行するタスクの基底クラス。start/stop/run/handle を定義する。
"""
from logger import Logger
import asyncio
from abc import ABC, abstractmethod
from error import Error
import threading
import uuid


class BackgroundPresentationUtilsBase(ABC):
    """
    バックグラウンドタスクの抽象基底クラス。

    非同期で start/stop し、run 内で handle を繰り返し呼ぶ。サブクラスで name と handle を実装する。
    """

    def __init__(
        self,
        logger: Logger,
    ):
        """
        基底を初期化する。

        :param Logger logger: ロガー
        """
        self.logger = logger
        self.task: asyncio.Task | None = None
        self.event = threading.Event()

    @property
    @abstractmethod
    def name(self) -> str:
        """タスク名を返す。サブクラスで実装する。"""
        pass

    async def start(self) -> None:
        """
        バックグラウンドタスクを起動する。run を非同期で開始する。
        """
        self.task = asyncio.create_task(self.run())
        self.event.clear()

    async def stop(self) -> None:
        """
        バックグラウンドタスクを停止する。イベントをセットし、タスクをキャンセルする。
        """
        if self.task:
            self.event.set()
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                self.logger.unexpected_error(exception=e, id=self.name)

    async def run(self) -> None:
        """
        イベントがセットされるまで、handle をスレッドで繰り返し実行する。
        """
        while not self.event.is_set():
            process_id = str(uuid.uuid4())
            try:
                self.logger.background_info(
                    process_id=process_id,
                    name=self.name,
                    message=f"background started",
                )
                await asyncio.to_thread(self.handle, process_id=process_id)
                self.logger.background_info(
                    process_id=process_id,
                    name=self.name,
                    message=f"background finished",
                )
            except Error as e:
                self.logger.error(error=e, id=process_id)
                continue
            except Exception as e:
                self.logger.unexpected_error(exception=e, id=process_id)
                continue

    @abstractmethod
    def handle(self, process_id: str) -> None:
        """
        1回分のタスク処理を行う。サブクラスで実装する。

        :param str process_id: プロセスID（ログ用）
        """
        pass
