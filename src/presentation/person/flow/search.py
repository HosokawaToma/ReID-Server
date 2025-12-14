from presentation import PresentationBase
from presentation import PresentationLogger
from presentation import PresentationRequest
from presentation import PresentationJSONResponse
from applications.person.flow.search import ApplicationPersonFlowSearch
from applications.person.flow.search import ApplicationPersonFlowSearchParams
from environment import Environment
from datetime import datetime
import uuid


class PresentationPersonFlowSearchRequest(PresentationRequest):
    person_id: uuid.UUID
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None

class PresentationPersonFlowSearch(PresentationBase):
    router_path = "/person/flow/search"
    methods = ["POST"]
    tags = ["Person Flow"]
    summary = "Search person flows"
    description = "Search person flows"
    responses = {
        200: {
            "description": "Person flows",
            "content": {"application/json": {"example": [{"id": "123e4567-e89b-12d3-a456-426614174000", "name": "John Doe"}]}},
        },
    }

    def __init__(
        self,
        logger: PresentationLogger,
        application: ApplicationPersonFlowSearch,
    ):
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "PresentationPersonFlowSearch":
        return cls(
            logger=PresentationLogger(),
            application=ApplicationPersonFlowSearch.create(environment=environment),
        )

    async def handle(self, request: PresentationPersonFlowSearchRequest):
        params = ApplicationPersonFlowSearchParams(
            person_id=request.person_id,
            timestamp_after=request.timestamp_after,
            timestamp_before=request.timestamp_before,
        )
        items = self.application.search(params=params)
        return PresentationJSONResponse(status=200, content={
            "person_flows": [
                {
                    "person_id": str(item.person_id),
                    "source_camera_id": item.source_camera_id,
                    "target_camera_id": item.target_camera_id,
                    "source_timestamp": item.source_timestamp.isoformat(),
                    "target_timestamp": item.target_timestamp.isoformat(),
                } for item in items
            ],
        })
