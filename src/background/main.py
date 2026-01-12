from environment import Environment
from background.presentations.person.snapshot.create import BackgroundPersonSnapshotCreate
from background.presentations.person.snapshot.feature_extraction import BackgroundPersonSnapshotFeatureExtraction
from background.presentations.person.snapshot.identify import BackgroundPersonSnapshotIdentify
from background.presentations.person.snapshot.junk_detection import BackgroundPersonSnapshotJunkDetection
import asyncio

class BackgroundMain:
    def __init__(
        self,
        person_snapshot_create: BackgroundPersonSnapshotCreate,
        person_snapshot_feature_extraction: BackgroundPersonSnapshotFeatureExtraction,
        person_snapshot_identify: BackgroundPersonSnapshotIdentify,
        person_snapshot_junk_detection: BackgroundPersonSnapshotJunkDetection,
    ):
        self.person_snapshot_create = person_snapshot_create
        self.person_snapshot_feature_extraction = person_snapshot_feature_extraction
        self.person_snapshot_identify = person_snapshot_identify
        self.person_snapshot_junk_detection = person_snapshot_junk_detection

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundMain":
        return cls(
            person_snapshot_create=BackgroundPersonSnapshotCreate.create(environment=environment),
            person_snapshot_feature_extraction=BackgroundPersonSnapshotFeatureExtraction.create(environment=environment),
            person_snapshot_identify=BackgroundPersonSnapshotIdentify.create(environment=environment),
            person_snapshot_junk_detection=BackgroundPersonSnapshotJunkDetection.create(environment=environment),
        )

    async def run(self):
        await self.person_snapshot_create.start()
        await self.person_snapshot_feature_extraction.start()
        await self.person_snapshot_identify.start()
        await self.person_snapshot_junk_detection.start()
        await asyncio.Event().wait()

if __name__ == "__main__":
    background_main = BackgroundMain.create(environment=Environment())
    asyncio.run(background_main.run())
