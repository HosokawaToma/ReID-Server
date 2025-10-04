"""add_initial_cameras_data

Revision ID: f041f316d866
Revises: 4db14631697e
Create Date: 2025-10-04 18:23:00.864341

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

cameras_table = sa.table('cameras',
                         sa.column('client_id', sa.String),
                         sa.column('camera_id', sa.Integer),
                         sa.column('view_id', sa.Integer)
                         )


# revision identifiers, used by Alembic.
revision: str = 'f041f316d866'
down_revision: Union[str, Sequence[str], None] = '4db14631697e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.bulk_insert(cameras_table, [
        {'client_id': 'admin', 'camera_id': 0, 'view_id': 0},
    ])


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        cameras_table.delete().where(cameras_table.c.client_id.in_(['admin']))
    )
