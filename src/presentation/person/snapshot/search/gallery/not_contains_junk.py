from presentation.utils.base import PresentationUtilBase
from logger import Logger
from presentation.utils.authenticated import PresentationUtilAdminClientAuthenticated
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from presentation.utils.type import PresentationUtilPathUUID
from applications.person.snapshot.search import ApplicationPersonSnapshotSearch
from dto.id import DtoId

class PresentationPersonSnapshotSearchGalleryNotContainsJunk(PresentationUtilBase):
    router_path = "/person/snapshot/search/gallery/not_contains_junk/{person_snapshot_id}"
    methods = ["POST"]
    tags = ["Person Snapshot"]
    summary = "Search person snapshots gallery not contains junk"
    description = "Search person snapshots gallery not contains junk"
    responses = {
        200: {
            "description": "Person snapshots gallery not contains junk found",
        },
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonSnapshotSearchGalleryNotContainsJunk":
        return cls(
            logger=Logger("presentation_person_snapshot_search_gallery_not_contains_junk"),
        )

    async def handle(
        self,
        admin_client_id: PresentationUtilAdminClientAuthenticated,
        person_snapshot_id: PresentationUtilPathUUID,
        application: ApplicationPersonSnapshotSearch = get_application(ApplicationPersonSnapshotSearch),
    ):
        ids = application.search_gallery_not_contains_junk(person_snapshot_id=DtoId(id=person_snapshot_id))
        return PresentationUtilJSONResponse(status=200, content={
            "person_snapshot_gallery_ids": [str(id.id) for id in ids],
        })
