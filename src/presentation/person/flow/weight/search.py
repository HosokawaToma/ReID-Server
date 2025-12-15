from applications.person.flow.weight.search import ApplicationPersonFlowWeightSearch
from applications.person.flow.weight.search import ApplicationPersonFlowWeightSearchParams
from presentation import PresentationBase
from presentation import PresentationAdminClientAuthenticated
from presentation import PresentationLogger
from presentation import PresentationRequestBody
from presentation import PresentationJSONResponse
from environment import Environment
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class PresentationPersonFlowWeightSearchRequest(PresentationRequestBody):
    person_ids: list[uuid.UUID] | None = None
    timestamp_after: datetime | None = None
    timestamp_before: datetime | None = None

class PresentationPersonFlowWeightSearch(PresentationBase):
    router_path = "/person/flow/weight/search"
    methods = ["POST"]
    tags = ["Person Flow"]
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
        admin_client_id: PresentationAdminClientAuthenticated,
        request: PresentationPersonFlowWeightSearchRequest | None = None,
    ):
        params = None
        if request is not None :
            params = ApplicationPersonFlowWeightSearchParams(
                person_ids=request.person_ids,
                timestamp_after=request.timestamp_after,
                timestamp_before=request.timestamp_before,
            )
        items = self.application_person_flow_weight_search.search(params=params)
        return PresentationJSONResponse(
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
