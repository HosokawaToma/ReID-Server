"""
マイグレーション用基底

SQLAlchemy の declarative_base を提供する。
"""
from sqlalchemy.orm import declarative_base

Base = declarative_base()
