from presentation import PresentationBase
from presentation import PresentationRequest
from presentation import PresentationRequestBody
from presentation import PresentationJSONResponse
from presentation import PresentationAdminClientAuthenticated
from applications.person.flow.search import ApplicationPersonFlowSearch
from applications.person.flow.search import ApplicationPersonFlowSearchParams
from applications.person.flow.search import ApplicationPersonFlowSearchNoFlowsFoundError
from environment import Environment
from logger import Logger
from datetime import datetime
import uuid

class PresentationPersonFlowSearchRequestBody(PresentationRequestBody):
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
        logger: Logger,
        application: ApplicationPersonFlowSearch,
    ):
        super().__init__(logger=logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "PresentationPersonFlowSearch":
        return cls(
            logger=Logger("presentation_person_flow_search"),
            application=ApplicationPersonFlowSearch.create(environment=environment),
        )

    async def handle(
        self,
        admin_client_id: PresentationAdminClientAuthenticated,
        request: PresentationRequest,
        body: PresentationPersonFlowSearchRequestBody,
    ):
        params = ApplicationPersonFlowSearchParams(
            person_id=body.person_id,
            timestamp_after=body.timestamp_after,
            timestamp_before=body.timestamp_before,
        )
        try:
            items = self.application.search(params=params)
        except ApplicationPersonFlowSearchNoFlowsFoundError as error:
            self.logger.api_response_info(request_id=request.get_request_id(), response_status_code=404)
            return PresentationJSONResponse(status=404, content={
                "message": "Person flows not found",
            })
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
