"""Add created_at and updated_at to todos

Revision ID: 4c301a1ce0a5
Revises: 807ac2c2f900
Create Date: 2024-07-23 21:54:51.886089

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func



# revision identifiers, used by Alembic.
revision: str = '4c301a1ce0a5'
down_revision: Union[str, None] = '807ac2c2f900'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('todos', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('todos', sa.Column('updated_at', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('todos', 'created_at')
    op.drop_column('todos', 'updated_at')