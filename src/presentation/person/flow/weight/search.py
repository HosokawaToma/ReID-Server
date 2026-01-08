from applications.person.flow.weight.search import ApplicationPersonFlowWeightSearch
from applications.person.flow.weight.search import ApplicationPersonFlowWeightSearchParams
from applications.person.flow.weight.search import ApplicationPersonFlowWeightSearchError
from presentation import PresentationBase
from presentation import PresentationAdminClientAuthenticated
from presentation import PresentationRequest
from logger import Logger
from presentation import PresentationRequestBody
from presentation import PresentationJSONResponse
from environment import Environment
from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class PresentationPersonFlowWeightSearchRequestBody(PresentationRequestBody):
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
        logger: Logger,
        application_person_flow_weight_search: ApplicationPersonFlowWeightSearch,
    ):
        super().__init__(logger=logger)
        self.application_person_flow_weight_search = application_person_flow_weight_search

    @classmethod
    def create(cls, environment: Environment) -> "PresentationPersonFlowWeightSearch":
        return cls(
            logger=Logger("presentation_person_flow_weight_search"),
            application_person_flow_weight_search=ApplicationPersonFlowWeightSearch.create(environment=environment),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        request: PresentationRequest,
        body: PresentationPersonFlowWeightSearchRequestBody | None = None,
    ):
        params = None
        if body is not None:
            params = ApplicationPersonFlowWeightSearchParams(
                person_ids=body.person_ids,
                timestamp_after=body.timestamp_after,
                timestamp_before=body.timestamp_before,
            )
        try:
            items = self.application_person_flow_weight_search.search(params=params)
        except ApplicationPersonFlowWeightSearchError as error:
            self.logger.api_response_info(request_id=request.get_request_id(), response_status_code=404)
            return PresentationJSONResponse(status=404, content={
                "message": "Person flow weight not found",
            })
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
