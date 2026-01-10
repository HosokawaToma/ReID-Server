"""
Environmentのユニットテスト
"""
import os
import pytest
from unittest.mock import patch

from environment import Environment


class TestEnvironment:
    """Environmentのテストクラス"""

    DEFAULT_ENV_VARS = {
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

    @pytest.mark.unit
    def test_環境変数が正しく読み込まれる(self):
        """環境変数が正しく読み込まれることを確認"""
        with patch.dict(os.environ, self.DEFAULT_ENV_VARS):
            env = Environment()

            assert env.app_host == "127.0.0.1"
            assert env.app_port == 8000
            assert env.hash_key == "test_hash_key"
            assert env.is_delete_unnecessary_images is False

    @pytest.mark.unit
    def test_必須環境変数が設定されていない場合に例外が発生する(self):
        """必須環境変数が設定されていない場合に例外が発生することを確認"""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError):
                Environment()

    @pytest.mark.unit
    def test_整数値が正しくパースされる(self):
        """整数値の環境変数が正しくパースされることを確認"""
        with patch.dict(os.environ, self.DEFAULT_ENV_VARS):
            env = Environment()

            assert isinstance(env.app_port, int)
            assert env.app_port == 8000
            assert isinstance(env.jwt_expire_minutes, int)
            assert env.jwt_expire_minutes == 30

    @pytest.mark.unit
    def test_不正な整数値で例外が発生する(self):
        """不正な整数値で例外が発生することを確認"""
        env_vars = self.DEFAULT_ENV_VARS.copy()
        env_vars["APP_PORT"] = "not_a_number"
        with patch.dict(os.environ, env_vars):
            with pytest.raises(ValueError):
                Environment()

    @pytest.mark.unit
    def test_ブール値が正しくパースされる(self):
        """ブール値の環境変数が正しくパースされることを確認"""
        test_cases = [
            ("true", True),
            ("True", True),
            ("1", True),
            ("yes", True),
            ("Yes", True),
            ("YES", True),
            ("false", False),
            ("False", False),
            ("0", False),
            ("no", False),
            ("No", False),
            ("NO", False),
        ]

        for bool_str, expected in test_cases:
            env_vars = self.DEFAULT_ENV_VARS.copy()
            env_vars["IS_DELETE_UNNECESSARY_IMAGES"] = bool_str
            with patch.dict(os.environ, env_vars):
                env = Environment()
                assert env.is_delete_unnecessary_images == expected


    @pytest.mark.unit
    def test_不正なブール値で例外が発生する(self):
        """不正なブール値で例外が発生することを確認"""
        env_vars = self.DEFAULT_ENV_VARS.copy()
        env_vars["IS_DELETE_UNNECESSARY_IMAGES"] = "invalid"
        with patch.dict(os.environ, env_vars):
            with pytest.raises(ValueError):
                Environment()
