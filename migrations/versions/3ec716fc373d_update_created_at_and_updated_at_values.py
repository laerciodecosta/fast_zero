"""Update created_at and updated_at values

Revision ID: 3ec716fc373d
Revises: 4c301a1ce0a5
Create Date: 2024-07-23 21:59:13.616710

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ec716fc373d'
down_revision: Union[str, None] = '4c301a1ce0a5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
