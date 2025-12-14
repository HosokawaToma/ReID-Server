from environment import Environment
from applications.person.snapshot.image.search import ApplicationPersonSnapshotImageSearch
from applications.person.snapshot.image.search import ApplicationPersonSnapshotImageSearchParams
from applications.person.snapshot.image.search import ApplicationPersonSnapshotImageSearchError
from presentation import PresentationBase
from presentation import PresentationLogger
from presentation import PresentationResponse
from presentation import PresentationImageResponse
import uuid

class PresentationPersonSnapshotImageSearch(PresentationBase):
    @property
    def router_path(self) -> str:
        return "/person/snapshot/image/search/{id}"

    @property
    def methods(self) -> list[str]:
        return ["GET"]

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

    async def handle(self, id: uuid.UUID):
        try:
            person_snapshot = self.application_person_snapshot_image_search.search(
                ApplicationPersonSnapshotImageSearchParams(id=id)
            )
            return PresentationImageResponse(status=200, image=person_snapshot.image)
        except ApplicationPersonSnapshotImageSearchError as e:
            return PresentationResponse(
                status=404,
                content={
                    "message": "Person snapshot image not found",
                },
            )
        except Exception as e:
            self.logger.error(f"Error searching person snapshot image: {e}")
            return PresentationResponse(
                status=500,
                content={
                    "message": "Internal server error",
                },
            )

