"""
テスト用の共通フィクスチャを定義
"""
import os
import sys
from pathlib import Path
from typing import Generator
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from environment import Environment
from main import ServerApp


@pytest.fixture
def mock_environment() -> Generator[Environment, None, None]:
    """
    テスト用のモック環境変数を提供するフィクスチャ
    """
    env_vars = {
        "APP_HOST": "127.0.0.1",
        "APP_PORT": "8000",
        "HASH_KEY": "test_hash_key",
        "PUBLIC_IP": "127.0.0.1",
        "ADMIN_CLIENT_ID": "test_client_id",
        "ADMIN_CLIENT_PASSWORD": "test_password",
        "IS_DELETE_UNNECESSARY_IMAGES": "false",
        "JWT_SECRET_KEY": "test_jwt_secret_key",
        "JWT_ALGORITHM": "HS256",
        "JWT_EXPIRE_MINUTES": "30",
        "JWT_REFRESH_SECRET_KEY": "test_refresh_secret_key",
        "JWT_REFRESH_ALGORITHM": "HS256",
        "JWT_REFRESH_EXPIRE_MINUTES": "1440",
        "POSTGRESQL_HOST": "localhost",
        "POSTGRESQL_PORT": "5432",
        "POSTGRESQL_DATABASE": "test_db",
        "POSTGRESQL_USER": "test_user",
        "POSTGRESQL_PASSWORD": "test_password",
        "STORAGE_DIRECTORY_NAME": "/tmp/test_storage",
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379",
        "REDIS_DB": "0",
        "COTURN_PORT": "3478",
        "COTURN_SECRET": "test_coturn_secret",
        "COTURN_TTL": "86400",
        "COTURN_USERNAME": "test_coturn_user",
        "COTURN_CREDENTIAL": "test_coturn_credential",
    }

    with patch.dict(os.environ, env_vars):
        yield Environment()


@pytest.fixture
def test_app(mock_environment: Environment) -> Generator[ServerApp, None, None]:
    """
    テスト用のFastAPIアプリケーションを提供するフィクスチャ
    """
    app = ServerApp.create(environment=mock_environment)

    # ミドルウェアとルートを設定（run()メソッドの内容を実行）
    from fastapi.middleware.cors import CORSMiddleware
    from logger import Logger
    from presentation import PresentationMiddleware

    app.fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.fastapi_app.add_middleware(
        PresentationMiddleware,
        logger=Logger("presentation_middleware"),
    )
    app.background_person_snapshot_create.setup(app.fastapi_app)
    app.background_person_snapshot_feature_extraction.setup(app.fastapi_app)
    app.background_person_snapshot_identify.setup(app.fastapi_app)
    app.background_person_snapshot_junk_detection.setup(app.fastapi_app)
    app.admin_auth_login.setup(app.fastapi_app)
    app.admin_auth_token_refresh.setup(app.fastapi_app)
    app.person_snapshot_create.setup(app.fastapi_app)
    app.person_snapshot_refresh.setup(app.fastapi_app)
    app.person_snapshot_search.setup(app.fastapi_app)
    app.person_flow_search.setup(app.fastapi_app)
    app.person_flow_weight_search.setup(app.fastapi_app)
    app.person_snapshot_image_search.setup(app.fastapi_app)
    app.frame_search.setup(app.fastapi_app)
    app.frame_image_search.setup(app.fastapi_app)
    app.presentation_exception_handler.setup(app.fastapi_app)

    yield app


@pytest.fixture
def client(test_app: ServerApp) -> Generator[TestClient, None, None]:
    """
    テスト用のHTTPクライアントを提供するフィクスチャ
    """
    with TestClient(test_app.fastapi_app) as test_client:
        yield test_client

