"""
ロガーモジュール

API・バックグラウンド・エラーのログ出力を提供する。
"""
import logging
from error import Error
from types import TracebackType
import traceback
import datetime
import zoneinfo


class Logger:
    """
    アプリケーション用ロガークラス。

    ストリームとファイルにログを出力し、API・バックグラウンド・エラー用のメソッドを提供する。
    """

    def __init__(self, name: str):
        """
        ロガーを初期化する。同名のロガーはストリームとファイルハンドラを設定する。

        :param str name: ロガー名（ファイル名のプレフィックスにも使用）
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.addHandler(logging.FileHandler(f"{name}.log"))

    def _traceback(self, exc_traceback: TracebackType):
        stack_summary = traceback.extract_tb(exc_traceback)
        return "->\n".join([f"{summary.filename}:{summary.lineno}:{summary.name}" for summary in stack_summary])

    def _timestamp(self):
        return datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo")).isoformat()

    def unexpected_error(self, exception: Exception, id: str) -> None:
        """
        予期しない例外をエラーログに出力する。

        :param Exception exception: 例外
        :param str id: リクエスト/プロセスID（ログ用）
        """
        self.logger.error(f"""Unexpected error: id: {id}
    Error: {exception.__class__.__name__} -> {str(exception)}
    Timestamp: {self._timestamp()}
    Traceback: {self._traceback(exception.__traceback__) if exception.__traceback__ is not None else None}
"""
                          )

    def error(self, error: Error, id: str) -> None:
        """
        アプリケーションエラーをエラーログに出力する。

        :param Error error: エラー
        :param str id: リクエスト/プロセスID（ログ用）
        """
        self.logger.error(f"""Error: id: {id}
    Error: {error.__class__.__name__} -> {error.message}
    Timestamp: {self._timestamp()}
    Traceback: {self._traceback(error.__traceback__) if error.__traceback__ is not None else None}
""")

    def api_request_info(self, request_id: str, request_path: str, request_method: str) -> None:
        """
        APIリクエストをINFOログに出力する。

        :param str request_id: リクエストID
        :param str request_path: パス
        :param str request_method: HTTPメソッド
        """
        self.logger.info(f"""API Request: id: {request_id}, path: {request_path}, method: {request_method}
    Timestamp: {self._timestamp()}
""")

    def api_response_info(self, request_id: str, response_status_code: int) -> None:
        """
        APIレスポンスをINFOログに出力する。

        :param str request_id: リクエストID
        :param int response_status_code: ステータスコード
        """
        self.logger.info(f"""API Response: id: {request_id}, status: {response_status_code}
    Timestamp: {self._timestamp()}
""")

    def background_info(self, process_id: str, name: str, message: str) -> None:
        """
        バックグラウンドタスクの情報をINFOログに出力する。

        :param str process_id: プロセスID
        :param str name: タスク名
        :param str message: メッセージ
        """
        self.logger.info(f"""Background: id: {process_id}, name: {name}, message: {message}
    Timestamp: {self._timestamp()}
""")
