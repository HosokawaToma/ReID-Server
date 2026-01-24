from fastapi import Depends
from typing import Any, Annotated, Sequence
from enum import Enum
from logger import Logger
from fastapi import FastAPI
from presentation.utils.response import PresentationUtilJSONResponse, PresentationUtilImageResponse
from abc import ABC, abstractmethod

class PresentationUtilBase(ABC):
    router_path: str
    methods: list[str]
    tags: list[str | Enum] | None = None
    summary: str | None = None
    description: str | None = None
    responses: dict[int | str, dict[str, Any]] | None = None
    dependencies: Sequence[Annotated[Any, Depends]] | None = None

    def __init__(self, logger: Logger):
        self.logger = logger

    def setup(self, app: FastAPI):
        app.add_api_route(
            self.router_path,
            self.handle,
            methods=self.methods,
            tags=self.tags,
            summary=self.summary,
            description=self.description,
            responses=self.responses,
            dependencies=self.dependencies,
        )

    @abstractmethod
    async def handle(self, *args, **kwargs) -> PresentationUtilJSONResponse | PresentationUtilImageResponse:
        pass
