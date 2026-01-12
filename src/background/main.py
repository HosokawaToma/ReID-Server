from environment import Environment
from background.presentations.person.snapshot.create import BackgroundPersonSnapshotCreate
from background.presentations.person.snapshot.feature_extraction import BackgroundPersonSnapshotFeatureExtraction
from background.presentations.person.snapshot.identify import BackgroundPersonSnapshotIdentify
from background.presentations.person.snapshot.junk_detection import BackgroundPersonSnapshotJunkDetection
import asyncio
import signal

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
        event = asyncio.Event()
        loop = asyncio.get_running_loop()
        loop.add_signal_handler(signal.SIGINT, event.set)
        loop.add_signal_handler(signal.SIGTERM, event.set)
        try:
            await self.start()
            await event.wait()
        finally:
            await self.stop()

    async def start(self):
        await self.person_snapshot_create.start()
        await self.person_snapshot_feature_extraction.start()
        await self.person_snapshot_identify.start()
        await self.person_snapshot_junk_detection.start()

    async def stop(self):
        await self.person_snapshot_create.stop()
        await self.person_snapshot_feature_extraction.stop()
        await self.person_snapshot_identify.stop()
        await self.person_snapshot_junk_detection.stop()

if __name__ == "__main__":
    background_main = BackgroundMain.create(environment=Environment())
    asyncio.run(background_main.run())
