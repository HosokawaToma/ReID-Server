from re import S
from presentation import PresentationBase
from presentation import PresentationLogger
from presentation import PresentationRequest
from presentation import PresentationResponse
from applications.person.flow.search import ApplicationPersonFlowSearch
from applications.person.flow.search import ApplicationPersonFlowSearchParams
from environment import Environment
from datetime import datetime
import uuid


class PresentationPersonFlowSearchRequest(PresentationRequest):
    after_timestamp: datetime | None = None
    before_timestamp: datetime | None = None
    person_ids: list[uuid.UUID] | None = None

class PresentationPersonFlowSearch(PresentationBase):
    @property
    def router_path(self) -> str:
        return "/person/flow/search"

    @property
    def methods(self) -> list[str]:
        return ["POST"]

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

    async def handle(self, request: PresentationPersonFlowSearchRequest) -> PresentationResponse:
        try:
            params = ApplicationPersonFlowSearchParams(
                after_timestamp=request.after_timestamp,
                before_timestamp=request.before_timestamp,
                person_ids=request.person_ids,
            )
            sequence_person_flows = self.application.search(params=params)
            return PresentationResponse(status=200, content={
                "person_flows": [
                    sequence_person_flow.to_json() for sequence_person_flow in sequence_person_flows
                ],
            })
        except Exception as e:
            self.logger.error(f"Error searching person flows: {e}")
            return PresentationResponse(status=500, content={"message": "Internal server error"})
