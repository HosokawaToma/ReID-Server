from presentation.utils.base import PresentationUtilBase
from logger import Logger
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.type import PresentationUtilPathDate, PresentationUtilPathInt
from applications.person.snapshot.search import ApplicationPersonSnapshotSearch
from dto.date import DtoDate



class PresentationPersonSnapshotSearchQueryIsJunk(PresentationUtilBase):
    router_path = "/person/snapshot/search/query/is_junk/{date}/{page}"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Search person snapshots query is junk"
    description = "Search person snapshots query is junk"
    responses = {
        200: {
            "description": "Person snapshots query is junk found",
        },
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotSearchQueryIsJunk":
        return cls(
            logger=Logger("presentation_person_snapshot_search_query_is_junk"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        date: PresentationUtilPathDate,
        page: PresentationUtilPathInt,
        application: ApplicationPersonSnapshotSearch = get_application(ApplicationPersonSnapshotSearch),
    ):
        ids = application.search_query_is_junk(
            date=DtoDate(year=date.year, month=date.month, day=date.day),
            page=page,
        )
        pagination = application.search_query_is_junk_paging(
            date=DtoDate(year=date.year, month=date.month, day=date.day),
        )
        return PresentationUtilJSONResponse(status=200, content={
            "person_snapshot_query_ids": [
                str(id.id) for id in ids
            ],
            "pagination": {
                "total_items": pagination.total_items,
                "total_pages": pagination.total_pages,
            },
        })
