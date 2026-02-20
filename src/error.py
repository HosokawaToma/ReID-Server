"""
アプリケーション用エラー定義

HTTPステータスに対応するカスタム例外と、システム・クライアント・ビジネスエラーの階層を定義する。
"""


class Error(Exception):
    """
    カスタムエラークラスの基底クラス
    :param str message: エラーの詳細情報
    """

    def __init__(self, message: str):
        """
        エラーを初期化する。

        :param str message: エラーメッセージ
        """
        self.message = message


class CustomSystemError(Error):
    """
    システムエラークラスの基底クラス
    アプリケーションのバグやインフラの問題など、想定外の事態に発生するエラー
    :param str message: エラーの詳細情報
    """
    pass


class InternalServerError(CustomSystemError):
    """
    内部サーバーエラークラス
    予期せぬ例外の発生に対して投げるエラー
    HTTPステータス: `500 Internal Server Error`
    :param str message: エラーの詳細情報
    """
    pass


class BadGatewayError(CustomSystemError):
    """
    外部連携エラークラス
    外部システムが原因の予期せぬ例外の発生に対して投げるエラー
    HTTPステータス: `502 Bad Gateway`
    :param str message: エラーの詳細情報
    """
    pass


class ServiceUnavailableError(CustomSystemError):
    """
    サービス利用不可エラークラス
    サーバーが一時的にリクエストを処理できない場合に対して投げるエラー
    HTTPステータス: `503 Service Unavailable`
    :param str message: エラーの詳細情報
    """
    pass


class GatewayTimeoutError(CustomSystemError):
    """
    ゲートウェイタイムアウトエラークラス
    処理が規定時間内に終わらなかった場合に対して投げるエラー
    HTTPステータス: `504 Gateway Timeout`
    :param str message: エラーの詳細情報
    """
    pass


class ClientError(Error):
    """
    クライアントエラークラスの基底クラス
    クライアントのリクエスト内容に問題がある場合に発生するエラー
    :param str message: エラーの詳細情報
    """
    pass


class AuthenticationError(ClientError):
    """
    認証エラークラス
    不正なログイン情報に対して投げるエラー
    HTTPステータス: `401 Unauthorized`
    :param str message: エラーの詳細情報
    """
    pass


class AuthorizationError(ClientError):
    """
    認可エラークラス
    不正な権限アクセスに対して投げるエラー
    HTTPステータス: `403 Forbidden`
    :param str message: エラーの詳細情報
    """
    pass


class ValidationError(ClientError):
    """
    バリデーションエラークラス
    不正な入力形式に対して投げるエラー
    HTTPステータス: `400 Bad Request`
    :param str message: エラーの詳細情報
    """
    pass


class NotFoundError(ClientError):
    """
    未検出エラークラス
    不正なデータアクセスに対して投げるエラー
    HTTPステータス: `404 Not Found`
    :param str message: エラーの詳細情報
    """
    pass


class BusinessError(ClientError):
    """
    ビジネスロジックエラークラス
    仕様上不正な処理に対して投げるエラー
    :param str message: エラーの詳細情報
    """
    pass


class ConflictError(BusinessError):
    """
    競合エラークラス
    不正なデータ重複に対して投げるエラー
    HTTPステータス: `409 Conflict`
    :param str message: エラーの詳細情報
    """
    pass


class UnprocessableError(BusinessError):
    """
    処理不要エラークラス
    不正な業務ルール違反に対して投げるエラー
    HTTPステータス: `422 Unprocessable Entity`
    :param str message: エラーの詳細情報
    """
    pass


class TooManyRequestsError(ClientError):
    """
    レートリミットエラークラス
    不正なリクエスト数に対して投げるエラー
    HTTPステータス: `429 Too Many Requests`
    :param str message: エラーの詳細情報
    """
    pass


class PayloadTooLargeError(ClientError):
    """
    ペイロード過大エラークラス
    不正なデータ量に対して投げるエラー
    HTTPステータス: `413 Payload Too Large`
    :param str message: エラーの詳細情報
    """
    pass
