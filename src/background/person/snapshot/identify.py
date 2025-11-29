from background import Background, BackgroundJobError, BackgroundLogger
from applications.person.snapshot.background.identify import ApplicationPersonSnapshotBackgroundIdentify
from applications.person.snapshot.background.identify import ApplicationPersonSnapshotBackgroundIdentifyError
from applications.person.snapshot.background.identify import ApplicationPersonSnapshotMissingFeatureError
from applications.person.snapshot.background.identify import ApplicationPersonSnapshotNotFoundError
from applications.person.snapshot.background.identify import ApplicationPersonSnapshotThresholdError
from environment import Environment

class BackgroundPersonSnapshotIdentify(Background):
    @property
    def name(self) -> str:
        return "person snapshot identify"

    def __init__(
        self,
        application: ApplicationPersonSnapshotBackgroundIdentify,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.application = application

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundPersonSnapshotIdentify":
        return cls(
            application=ApplicationPersonSnapshotBackgroundIdentify.create(environment),
            logger=BackgroundLogger(),
        )

    async def process(self) -> None:
        try:
            await self.application.identify()
        except ApplicationPersonSnapshotMissingFeatureError:
            raise BackgroundJobError(f"Person snapshot missing feature")
        except ApplicationPersonSnapshotNotFoundError:
            raise BackgroundJobError(f"Person snapshot not found")
        except ApplicationPersonSnapshotThresholdError:
            raise BackgroundJobError(f"No matching people found")
