from presentation.utils.base import PresentationUtilBase
from logger import Logger
from presentation.utils.type import PresentationUtilPathDate, PresentationUtilPathInt
from presentation.utils.factory import get_application
from presentation.utils.response import PresentationUtilJSONResponse
from applications.reid.evaluation import ApplicationReidEvaluation
from dto.date import DtoDate

class PresentationReidEvaluation(PresentationUtilBase):
    router_path = "/reid/evaluation/{date}/{attempt}"
    methods = ["GET"]
    tags = ["reid"]
    summary = "再識別評価を行う"
    description = "再識別評価を行う"
    responses = {
        200: {
            "description": "再識別評価を行う",
        }
    }

    def __init__(self, logger: Logger):
        super().__init__(logger=logger)

    @classmethod
    def create(cls) -> "PresentationReidEvaluation":
        return cls(
            logger=Logger("presentation_reid_evaluation"),
        )

    async def handle(
        self,
        date: PresentationUtilPathDate,
        attempt: PresentationUtilPathInt,
        application: ApplicationReidEvaluation = get_application(ApplicationReidEvaluation),
    ) -> PresentationUtilJSONResponse:
        cmc_curve_is_not_junk, cmc_curve_is_junk, query_person_ids = application.calculate(
            date=DtoDate(year=date.year, month=date.month, day=date.day),
            attempt=attempt,
        )
        return PresentationUtilJSONResponse(status=200, content={
            "cmc_curve_is_not_junk": cmc_curve_is_not_junk.cmc_curve,
            "cmc_curve_is_junk": cmc_curve_is_junk.cmc_curve,
            "query_person_ids": [str(id.id) for id in query_person_ids],
        })
