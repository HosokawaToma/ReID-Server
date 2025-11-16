import fastapi
from fastapi.responses import JSONResponse
from applications.person_flow import ApplicationPersonFlow
from presentation.person_path.request import PresentationPersonPathRequest
from entities.person_flow_weight import EntityPersonFlowWeight

class PresentationPersonPath:
    def __init__(self, application_person_flow: ApplicationPersonFlow):
        self.application_person_flow = application_person_flow

    def setup(self, app: fastapi.FastAPI):
        app.add_api_route("/person_path", self.endpoint, methods=["GET"])

    async def endpoint(self, request: PresentationPersonPathRequest):
        person_flow_weights = self.application_person_flow.process(
            after_timestamp=request.after_timestamp,
            before_timestamp=request.before_timestamp,
        )
        return JSONResponse(content={"person_flow_weights": [weight.to_dict() for weight in person_flow_weights]})
