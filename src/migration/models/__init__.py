"""
マイグレーション用 ORM モデル

SQLAlchemy モデルと Alembic 用メタデータをエクスポートする。
"""
from .base import Base

ALEMBIC_MODELS = Base.metadata
