"""add_cameras_table

Revision ID: 4db14631697e
Revises: 01db91fbe39f
Create Date: 2025-10-04 18:22:51.541875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4db14631697e'
down_revision: Union[str, Sequence[str], None] = '01db91fbe39f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('cameras',
    sa.Column('client_id', sa.String(), nullable=False),
    sa.Column('camera_id', sa.Integer(), nullable=False),
    sa.Column('view_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['clients.id'], ),
    sa.PrimaryKeyConstraint('client_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('cameras')
