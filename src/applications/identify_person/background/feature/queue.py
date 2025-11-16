import asyncio
import uuid
from typing import Callable, Coroutine, Any

class ApplicationIdentifyPersonBackgroundFeatureQueue:
    queue= asyncio.Queue[tuple[uuid.UUID, Callable[[uuid.UUID], Coroutine[Any, Any, Any]] | None]]()

    async def add(self, id: uuid.UUID, callback: Callable[[uuid.UUID], Coroutine[Any, Any, Any]] | None = None):
        return await ApplicationIdentifyPersonBackgroundFeatureQueue.queue.put((id, callback))

    async def get(self) -> tuple[uuid.UUID, Callable[[uuid.UUID], Coroutine[Any, Any, Any]] | None]:
        return await ApplicationIdentifyPersonBackgroundFeatureQueue.queue.get()
