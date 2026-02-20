"""
プレゼンテーション基底

FastAPI にルートを 1 本登録し、リクエストを処理して JSON または画像レスポンスを返すための抽象基底を提供する。
サブクラスは router_path, methods, tags, summary, description, responses を定義し、handle で実際の処理を実装する。
"""
from fastapi import Depends
from typing import Any, Annotated, Sequence
from enum import Enum
from logger import Logger
from fastapi import FastAPI
from presentation.utils.response import PresentationUtilJSONResponse, PresentationUtilImageResponse
from abc import ABC, abstractmethod


class PresentationUtilBase(ABC):
    """
    プレゼンテーション層の抽象基底クラス。

    クラス属性で router_path（パス）、methods（HTTP メソッド一覧）、tags（OpenAPI タグ）、summary・description・responses（OpenAPI 用）を定義する。
    setup(app) で FastAPI アプリに add_api_route により 1 ルートとして登録する。リクエスト処理はサブクラスで handle を実装する。
    """
    router_path: str
    methods: list[str]
    tags: list[str | Enum] | None = None
    summary: str | None = None
    description: str | None = None
    responses: dict[int | str, dict[str, Any]] | None = None
    dependencies: Sequence[Annotated[Any, Depends]] | None = None

    def __init__(self, logger: Logger):
        """
        プレゼンテーションを初期化する。

        :param Logger logger: ロガー
        """
        self.logger = logger

    def setup(self, app: FastAPI) -> None:
        """
        ルートを FastAPI アプリに登録する。

        :param FastAPI app: FastAPIアプリケーション
        """
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
        """
        リクエストを処理し、JSONまたは画像レスポンスを返す。サブクラスで実装する。

        :return PresentationUtilJSONResponse | PresentationUtilImageResponse: レスポンス
        """
        pass
