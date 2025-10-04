"""add_initial_clients_data

Revision ID: 01db91fbe39f
Revises: b78fdd10d139
Create Date: 2025-09-29 15:02:07.599624

"""
from typing import Sequence, Union
import hashlib

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01db91fbe39f'
down_revision: Union[str, Sequence[str], None] = 'b78fdd10d139'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


clients_table = sa.table('clients',
                         sa.column('id', sa.String),
                         sa.column('hashed_password', sa.String)
                         )

def upgrade() -> None:
    """Upgrade schema."""
    hashed_password = hashlib.sha256('admin'.encode()).hexdigest()
    op.bulk_insert(clients_table, [
        {'id': 'admin', 'hashed_password': hashed_password},
    ])


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        clients_table.delete().where(clients_table.c.id.in_(['admin']))
    )
