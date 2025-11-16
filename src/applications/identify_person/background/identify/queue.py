import asyncio
import uuid

class ApplicationIdentifyPersonBackgroundIdentifyQueue:
    _queue: asyncio.Queue[uuid.UUID] | None = None

    def __init__(self):
        if self._queue is None:
            self._queue = asyncio.Queue[uuid.UUID]()

    async def add(self, id: uuid.UUID):
        if self._queue is None:
            raise ValueError("Queue is not initialized")
        await self._queue.put(id)

    async def get(self) -> uuid.UUID:
        if self._queue is None:
            raise ValueError("Queue is not initialized")
        return await self._queue.get()
