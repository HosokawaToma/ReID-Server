import asyncio
import uuid
from typing import Callable, Coroutine, Any

class ApplicationIdentifyPersonBackgroundFeatureQueue:
    _queue: asyncio.Queue[tuple[uuid.UUID, Callable[[uuid.UUID], Coroutine[Any, Any, Any]] | None]] | None = None

    def __init__(self):
        if self._queue is None:
            self._queue = asyncio.Queue[tuple[uuid.UUID, Callable[[uuid.UUID], Coroutine[Any, Any, Any]] | None]]()

    async def add(self, id: uuid.UUID, callback: Callable[[uuid.UUID], Coroutine[Any, Any, Any]] | None = None):
        if self._queue is None:
            raise ValueError("Queue is not initialized")
        return await self._queue.put((id, callback))

    async def get(self) -> tuple[uuid.UUID, Callable[[uuid.UUID], Coroutine[Any, Any, Any]] | None]:
        if self._queue is None:
            raise ValueError("Queue is not initialized")
        return await self._queue.get()
