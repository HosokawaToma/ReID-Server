import asyncio
import uuid

class ApplicationIdentifyPersonBackgroundIdentifyQueue:
    queue= asyncio.Queue[uuid.UUID]()

    async def add(self, id: uuid.UUID):
        await ApplicationIdentifyPersonBackgroundIdentifyQueue.queue.put(id)

    async def get(self) -> uuid.UUID:
        return await ApplicationIdentifyPersonBackgroundIdentifyQueue.queue.get()
