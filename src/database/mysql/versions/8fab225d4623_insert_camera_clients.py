"""insert camera_clients

Revision ID: 8fab225d4623
Revises: 179b25a76130
Create Date: 2025-10-31 01:17:12.916995

"""
from typing import Sequence, Union
import os
import json
import hashlib

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session


# revision identifiers, used by Alembic.
revision: str = '8fab225d4623'
down_revision: Union[str, Sequence[str], None] = '179b25a76130'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 環境変数からシードデータを読み込む
    seed_data_json = os.getenv("CAMERA_CLIENTS_SEED_DATA")

    if not seed_data_json:
        # 環境変数が設定されていない場合は何もしない
        return

    try:
        seed_data = json.loads(seed_data_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"環境変数CAMERA_CLIENTS_SEED_DATAのJSON形式が不正です: {e}")

    if not isinstance(seed_data, list):
        raise ValueError("環境変数CAMERA_CLIENTS_SEED_DATAは配列である必要があります")

    # テーブル定義を取得
    camera_clients_table = sa.Table(
        'camera_clients',
        sa.MetaData(),
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('hashed_password', sa.String(255)),
        sa.Column('camera_id', sa.Integer()),
        sa.Column('view_id', sa.Integer()),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )

    # データベース接続を取得
    bind = op.get_bind()
    session = Session(bind=bind)

    try:
        for item in seed_data:
            # 必須フィールドのチェック
            if not all(key in item for key in ['id', 'password', 'camera_id', 'view_id']):
                raise ValueError(f"必須フィールドが不足しています: {item}")

            # パスワードをハッシュ化
            hashed_password = hashlib.sha256(
                item['password'].encode()).hexdigest()

            # データを投入
            session.execute(
                camera_clients_table.insert().values(
                    id=item['id'],
                    hashed_password=hashed_password,
                    camera_id=item['camera_id'],
                    view_id=item['view_id'],
                    created_at=sa.func.now(),
                    updated_at=sa.func.now(),
                )
            )

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def downgrade() -> None:
    """Downgrade schema."""
    # 環境変数から削除対象のIDリストを読み込む
    seed_data_json = os.getenv("CAMERA_CLIENTS_SEED_DATA")

    if not seed_data_json:
        # 環境変数が設定されていない場合は何もしない
        return

    try:
        seed_data = json.loads(seed_data_json)
    except json.JSONDecodeError:
        # JSON形式が不正な場合は何もしない
        return

    if not isinstance(seed_data, list):
        return

    # テーブル定義を取得
    camera_clients_table = sa.Table(
        'camera_clients',
        sa.MetaData(),
        sa.Column('id', sa.String(255), primary_key=True),
    )

    # データベース接続を取得
    bind = op.get_bind()
    session = Session(bind=bind)

    try:
        # 投入したデータを削除
        for item in seed_data:
            if 'id' in item:
                session.execute(
                    camera_clients_table.delete().where(
                        camera_clients_table.c.id == item['id']
                    )
                )

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
