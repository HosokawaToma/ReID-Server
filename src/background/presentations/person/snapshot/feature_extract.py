from background.presentations.utils import BackgroundPresentationUtilsBase
from background.applications.person.snapshot.feature_extract import BackgroundApplicationPersonSnapshotFeatureExtract
from environment import Environment
from logger import Logger

class BackgroundPersonSnapshotFeatureExtract(BackgroundPresentationUtilsBase):
    def __init__(
        self,
        logger: Logger,
        application: BackgroundApplicationPersonSnapshotFeatureExtract,
    ):
        super().__init__(logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotFeatureExtract":
        return cls(
            logger=Logger("background_person_snapshot_feature_extract"),
            application=BackgroundApplicationPersonSnapshotFeatureExtract.create(environment),
        )

    @property
    def name(self) -> str:
        return "person_snapshot_feature_extract"

    def handle(self, process_id: str) -> None:
        id = self.application.extract()
        self.logger.background_info(
            process_id=process_id,
            name=self.name,
            message=f"person snapshot feature extracted: {id.id}",
        )
