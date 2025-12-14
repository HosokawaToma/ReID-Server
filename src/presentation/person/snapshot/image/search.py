from environment import Environment
from applications.person.snapshot.image.search import ApplicationPersonSnapshotImageSearch
from applications.person.snapshot.image.search import ApplicationPersonSnapshotImageSearchParams
from applications.person.snapshot.image.search import ApplicationPersonSnapshotImageSearchError
from presentation import PresentationBase
from presentation import PresentationAdminClientAuthenticated
from presentation import PresentationLogger
from presentation import PresentationJSONResponse
from presentation import PresentationImageResponse
import uuid

class PresentationPersonSnapshotImageSearch(PresentationBase):
    router_path = "/person/snapshot/image/search/{id}"
    methods = ["GET"]
    tags= ["Person Snapshot Image"]
    summary = "Search person snapshot image"
    description = "Search person snapshot image by image id"
    responses = {
        200: {
            "description": "Person snapshot image found",
        },
        404: {
            "description": "Person snapshot image not found",
        },
        500: {
            "description": "Internal server error",
        },
    }

    def __init__(
        self,
        logger: PresentationLogger,
        application_person_snapshot_image_search: ApplicationPersonSnapshotImageSearch
        ):
        super().__init__(logger=logger)
        self.application_person_snapshot_image_search = application_person_snapshot_image_search

    @classmethod
    def create(cls, environment: Environment) -> "PresentationPersonSnapshotImageSearch":
        return cls(
            logger=PresentationLogger(),
            application_person_snapshot_image_search=ApplicationPersonSnapshotImageSearch.create(environment),
        )

    async def handle(self, admin_client_id: PresentationAdminClientAuthenticated, id: uuid.UUID):
        try:
            person_snapshot = self.application_person_snapshot_image_search.search(
                ApplicationPersonSnapshotImageSearchParams(id=id)
            )
            return PresentationImageResponse(status=200, image=person_snapshot.image)
        except ApplicationPersonSnapshotImageSearchError as e:
            return PresentationJSONResponse(
                status=404,
                content={
                    "message": "Person snapshot image not found",
                },
            )
