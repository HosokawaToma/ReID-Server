from background import Background, BackgroundLogger
from applications.person.snapshot.background.identify import ApplicationPersonSnapshotBackgroundIdentify
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
        person_snapshot = self.application.identify()
        return f"person snapshot id: {person_snapshot.id} identified as person id: {person_snapshot.person_id}"
