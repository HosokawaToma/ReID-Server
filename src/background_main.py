from environment import Environment
from background.presentations.person.snapshot.create import BackgroundPersonSnapshotCreate
from background.presentations.person.snapshot.reid import BackgroundPersonSnapshotReid
import asyncio
import signal

class BackgroundMain:
    def __init__(
        self,
        person_snapshot_create: BackgroundPersonSnapshotCreate,
        person_snapshot_reid: BackgroundPersonSnapshotReid,
    ):
        self.person_snapshot_create = person_snapshot_create
        self.person_snapshot_reid = person_snapshot_reid

    @classmethod
    def create(cls, environment: Environment) -> "BackgroundMain":
        return cls(
            person_snapshot_create=BackgroundPersonSnapshotCreate.create(environment=environment),
            person_snapshot_reid=BackgroundPersonSnapshotReid.create(environment=environment),
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
        await self.person_snapshot_reid.start()

    async def stop(self):
        await self.person_snapshot_create.stop()
        await self.person_snapshot_reid.stop()

if __name__ == "__main__":
    background_main = BackgroundMain.create(environment=Environment())
    asyncio.run(background_main.run())
