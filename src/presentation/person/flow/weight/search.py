from applications.person.flow.weight.search import ApplicationPersonFlowWeightSearch
from applications.person.flow.weight.search import ApplicationPersonFlowWeightSearchParams
from presentation import PresentationBase
from presentation import PresentationLogger
from presentation import PresentationRequest
from presentation import PresentationResponse
from environment import Environment
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class PresentationPersonFlowWeightSearchRequest(PresentationRequest):
    person_ids: list[uuid.UUID] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None

class PresentationPersonFlowWeightSearch(PresentationBase):
    @property
    def router_path(self) -> str:
        return "/person/flow/weight/search"

    @property
    def methods(self) -> list[str]:
        return ["POST"]

    tags = ["Person Flow", "Person Flow Weight"]
    summary = "Search person flow weight"
    description = "Search person flow weight"
    responses = {
        200: {
            "description": "Person flow weight",
        }
    }

    def __init__(
        self,
        logger: PresentationLogger,
        application_person_flow_weight_search: ApplicationPersonFlowWeightSearch,
    ):
        super().__init__(logger=logger)
        self.application_person_flow_weight_search = application_person_flow_weight_search

    @classmethod
    def create(cls, environment: Environment) -> "PresentationPersonFlowWeightSearch":
        return cls(
            logger=PresentationLogger(),
            application_person_flow_weight_search=ApplicationPersonFlowWeightSearch.create(environment=environment),
        )

    async def handle(
        self,
        request: PresentationPersonFlowWeightSearchRequest,
    ) -> PresentationResponse:
        try:
            items = self.application_person_flow_weight_search.search(
                params=ApplicationPersonFlowWeightSearchParams(
                    person_ids=request.person_ids,
                    timestamp_after=request.timestamp_after,
                    timestamp_before=request.timestamp_before,
                ),
            )
            return PresentationResponse(
                status=200,
                content={
                    "weights": [
                        {
                            "target_camera_id": item.target_camera_id,
                            "source_camera_id": item.source_camera_id,
                            "weight": item.weight,
                        } for item in items
                    ]
                },
            )
        except Exception as e:
            self.logger.error(f"Error searching person flow weight: {e}")
            return PresentationResponse(
                status=500,
                content={"message": "Internal server error"},
            )
