"""
人物検出正解ラベル削除のプレゼンテーション層

POST /person/snapshot/answer/delete/{person_snapshot_id} で人物検出結果 ID を受け取り、その正解ラベル（person_id の紐付け）を削除する API を提供する。
認証済み管理クライアントのみ利用可能。成功時は 200 とメッセージを JSON で返す。
"""
from presentation.utils.base import PresentationUtilBase
from logger import Logger
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from dto.id import DtoId
from applications.person.snapshot.answer.delete import ApplicationPersonSnapshotAnswerDelete
from presentation.utils.type import PresentationUtilPathUUID


class PresentationPersonSnapshotAnswerDelete(PresentationUtilBase):
    """
    人物検出正解ラベル削除の API エンドポイントを提供するプレゼンテーションクラス。

    POST /person/snapshot/answer/delete/{person_snapshot_id} でパスに指定した人物検出結果の正解ラベルを削除する。評価用正解データの修正に用いる。成功時は 200 と {"message": "Answer label deleted"} を返す。Bearer トークン必須。
    """
    router_path = "/person/snapshot/answer/delete/{person_snapshot_id}"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Delete person snapshot answer"
    description = "Delete person snapshot answer"
    responses = {
        200: {"description": "Answer label deleted"},
    }

    def __init__(self, logger: Logger):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotAnswerDelete":
        """
        プレゼンテーションインスタンスを生成する。

        :return PresentationPersonSnapshotAnswerDelete: プレゼンテーションインスタンス
        """
        return cls(
            logger=Logger("presentation_person_snapshot_answer_delete"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        person_snapshot_id: PresentationUtilPathUUID,
        application: ApplicationPersonSnapshotAnswerDelete = get_application(
            ApplicationPersonSnapshotAnswerDelete),
    ):
        """
        指定した人物検出結果 ID の正解ラベルを削除し、成功メッセージを JSON で返す。

        パスの person_snapshot_id を DTO に渡し、アプリケーション層で該当する正解ラベルを削除する。存在しない ID の場合は NotFoundError により 404 となる。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント（Bearer 検証で注入）
        :param PresentationUtilPathUUID person_snapshot_id: 正解ラベルを削除する人物検出結果 ID（パス）
        :param ApplicationPersonSnapshotAnswerDelete application: 正解ラベル削除アプリケーション（Depends で注入）
        :return PresentationUtilJSONResponse: 200 と {"message": "Answer label deleted"}
        """
        application.delete(person_snapshot_id=DtoId(id=person_snapshot_id))
        return PresentationUtilJSONResponse(status=200, content={"message": "Answer label deleted"})
