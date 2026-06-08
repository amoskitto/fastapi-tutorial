"""add user table

Revision ID: 554da91625db
Revises: 2d12574ca6e0
Create Date: 2026-06-05 19:20:36.090228

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '554da91625db'
down_revision: Union[str, Sequence[str], None] = '2d12574ca6e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
