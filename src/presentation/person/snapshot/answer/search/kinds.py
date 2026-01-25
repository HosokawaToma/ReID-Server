from presentation.utils.base import PresentationUtilBase
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from logger import Logger
from applications.person.snapshot.answer.search.kinds import ApplicationPersonSnapshotAnswerSearchKinds

class PresentationPersonSnapshotAnswerSearchKinds(PresentationUtilBase):
    router_path = "/person/snapshot/answer/search/kinds"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Search person snapshot answer kinds"
    description = "Search person snapshot answer kinds"
    responses = {
        200: {
            "description": "Person snapshot answer kinds found",
        },
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotAnswerSearchKinds":
        return cls(
            logger=Logger("presentation_person_snapshot_answer_search_kinds"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        application: ApplicationPersonSnapshotAnswerSearchKinds = get_application(ApplicationPersonSnapshotAnswerSearchKinds),
    ):
        """
        人物検出結果の正解ラベルの種類を検索する
        :return PresentationUtilJSONResponse: 人物検出結果の正解ラベルの種類リスト
        :raises PresentationPersonSnapshotAnswerSearchKindsError: 人物検出結果の正解ラベルの種類検索に失敗した場合に発生するエラー
        """
        items = application.search()
        return PresentationUtilJSONResponse(
            status=200,
            content={
                "person_snapshot_answer_kinds": [
                    {
                        "id": str(item.id),
                        "person_id": str(item.person_id) if item.person_id is not None else None,
                        "is_junk": item.is_junk,
                    } for item in items
                ],
            },
        )
