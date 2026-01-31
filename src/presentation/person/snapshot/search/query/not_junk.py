from presentation.utils.base import PresentationUtilBase
from logger import Logger
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.type import PresentationUtilPathTimestamp, PresentationUtilPathInt
from applications.person.snapshot.search import ApplicationPersonSnapshotSearch
from dto.timestamp import DtoTimestamp


class PresentationPersonSnapshotSearchQueryNotJunk(PresentationUtilBase):
    router_path = "/person/snapshot/search/query/not_junk/{timestamp}/{page}"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Search person snapshots query not junk"
    description = "Search person snapshots query not junk"
    responses = {
        200: {
            "description": "Person snapshots query not junk found",
        },
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotSearchQueryNotJunk":
        return cls(
            logger=Logger("presentation_person_snapshot_search_query_not_junk"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        timestamp: PresentationUtilPathTimestamp,
        page: PresentationUtilPathInt,
        application: ApplicationPersonSnapshotSearch = get_application(
            ApplicationPersonSnapshotSearch),
    ):
        ids = application.search_query_not_junk(
            timestamp=DtoTimestamp(timestamp=timestamp), page=page)
        pagination = application.search_query_not_junk_paging(
            timestamp=DtoTimestamp(timestamp=timestamp))
        return PresentationUtilJSONResponse(status=200, content={
            "person_snapshot_query_ids": [
                str(id.id) for id in ids
            ],
            "pagination": {
                "total_items": pagination.total_items,
                "total_pages": pagination.total_pages,
            },
        })
