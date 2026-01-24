from applications.person.flow.weight.search import ApplicationPersonFlowWeightSearch
from dto.person.flow.weight.query import DtoPersonFlowWeightQuery
from presentation import PresentationBase
from presentation import PresentationAdminClientAuthenticated
from presentation import get_application
from presentation import PresentationRequest
from logger import Logger
from presentation import PresentationRequestBody
from presentation import PresentationJSONResponse
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PresentationPersonFlowWeightSearchRequestBody(PresentationRequestBody):
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
    ):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationPersonFlowWeightSearch":
        return cls(
            logger=Logger("presentation_person_flow_weight_search"),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        request: PresentationRequest,
        body: PresentationPersonFlowWeightSearchRequestBody | None = None,
        application: ApplicationPersonFlowWeightSearch = get_application(ApplicationPersonFlowWeightSearch),
    ):
        query = None
        if body is not None:
            query = DtoPersonFlowWeightQuery(
                timestamp_after=body.timestamp_after,
                timestamp_before=body.timestamp_before,
            )
        items = application.search(query=query)
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
