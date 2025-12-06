from background import Background, BackgroundJobError, BackgroundLogger
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotBackgroundFeatureExtraction
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotNotFoundError
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotImageNotFoundError
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotBackgroundFeatureExtractionError
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotYoloPoseNotFoundError
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotYoloPoseVerificationError
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotYoloSegmentationNotFoundError
from applications.person.snapshot.background.feature_extraction import ApplicationPersonSnapshotYoloSegmentationVerificationError
from environment import Environment

class BackgroundPersonSnapshotFeatureExtraction(Background):
    def __init__(
        self,
        logger: BackgroundLogger,
        application: ApplicationPersonSnapshotBackgroundFeatureExtraction,
    ):
        super().__init__(logger)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotFeatureExtraction":
        return cls(
            application=ApplicationPersonSnapshotBackgroundFeatureExtraction.create(environment),
            logger=BackgroundLogger(),
        )

    @property
    def name(self) -> str:
        return "person_snapshot_feature_extraction"

    async def process(self) -> str:
        try:
            person_snapshot = await self.application.extract()
            return f"person snapshot id: {person_snapshot.id} extracted"
        except ApplicationPersonSnapshotNotFoundError:
            raise BackgroundJobError("person snapshot not found")
        except ApplicationPersonSnapshotImageNotFoundError:
            raise BackgroundJobError("person snapshot image not found")
        except ApplicationPersonSnapshotYoloPoseNotFoundError:
            raise BackgroundJobError("person snapshot yolo pose not found")
        except ApplicationPersonSnapshotYoloPoseVerificationError:
            raise BackgroundJobError("person snapshot yolo pose verification error")
        except ApplicationPersonSnapshotYoloSegmentationNotFoundError:
            raise BackgroundJobError("person snapshot yolo segmentation not found")
        except ApplicationPersonSnapshotYoloSegmentationVerificationError:
            raise BackgroundJobError("person snapshot yolo segmentation verification error")
        except ApplicationPersonSnapshotBackgroundFeatureExtractionError:
            raise BackgroundJobError("person snapshot feature extraction error")
