from background import Background, BackgroundJobError, BackgroundLogger
from applications.person.snapshot.background.identify import ApplicationPersonSnapshotBackgroundIdentify
from applications.person.snapshot.background.identify import ApplicationPersonSnapshotBackgroundIdentifyError
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

    def handle(self) -> str:
        try:
            person_snapshot = self.application.identify()
            return f"person snapshot id: {person_snapshot.id} identified as person id: {person_snapshot.person_id}"
        except ApplicationPersonSnapshotBackgroundIdentifyError as e:
            raise BackgroundJobError(e.message)
