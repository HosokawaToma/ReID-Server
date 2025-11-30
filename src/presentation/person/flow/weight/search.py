from applications.person.flow.weigth.search import ApplicationPersonFlowWeightSearch
from applications.person.flow.weigth.search import ApplicationPersonFlowWeightSearchParams
from sequences.person.flow_weights import SequencePersonFlowWeights
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
    after_timestamp: datetime | None = None
    before_timestamp: datetime | None = None
    person_ids: list[uuid.UUID] | None = None

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
            params = ApplicationPersonFlowWeightSearchParams(
                after_timestamp=request.after_timestamp,
                before_timestamp=request.before_timestamp,
                person_ids=request.person_ids,
            )
            weights = self.application_person_flow_weight_search.search(params=params)
            return PresentationResponse(
                status=200,
                content=weights.to_json(),
            )
        except Exception as e:
            self.logger.error(f"Error searching person flow weight: {e}")
            return PresentationResponse(
                status=500,
                content={"message": "Internal server error"},
            )
