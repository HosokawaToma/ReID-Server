"""
人物検出正解ラベル削除のプレゼンテーション層

人物検出IDを受け取り、正解ラベルを削除してJSONで返す。
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
    人物検出正解ラベル削除のAPIエンドポイントを提供するプレゼンテーションクラス。
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
        指定した人物検出IDの正解ラベルを削除し、成功メッセージをJSONで返す。

        :param PresentationUtilAdminClientAuthenticated admin_client_id: 認証済み管理クライアント
        :param PresentationUtilPathUUID person_snapshot_id: 人物検出結果ID
        :param ApplicationPersonSnapshotAnswerDelete application: 正解ラベル削除アプリケーション
        :return PresentationUtilJSONResponse: 成功メッセージを含むJSONレスポンス
        """
        application.delete(person_snapshot_id=DtoId(id=person_snapshot_id))
        return PresentationUtilJSONResponse(status=200, content={"message": "Answer label deleted"})
