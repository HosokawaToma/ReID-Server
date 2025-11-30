from environment import Environment
from applications.person.snapshot.image.search import ApplicationPersonSnapshotImageSearch
from applications.person.snapshot.image.search import ApplicationPersonSnapshotImageSearchParams
from applications.person.snapshot.image.search import ApplicationPersonSnapshotImageSearchNotFoundError
from presentation import PresentationBase
from presentation import PresentationLogger
from presentation import PresentationResponse
from presentation import PresentationImageResponse
import uuid

class PresentationPersonSnapshotImageSearch(PresentationBase):
    @property
    def router_path(self) -> str:
        return "/person/snapshot/image/search/{image_id}"

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

    async def handle(self, image_id: uuid.UUID):
        try:
            image = self.application_person_snapshot_image_search.search(
                ApplicationPersonSnapshotImageSearchParams(image_id=image_id)
            )
            return PresentationImageResponse(status=200, image=image.image)
        except ApplicationPersonSnapshotImageSearchNotFoundError:
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

