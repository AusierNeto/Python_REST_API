"""Add favorites and products_snapshot tables on database

Revision ID: 80772b1b80dc
Revises: 387d2b1bfb87
Create Date: 2025-10-30 21:20:17.453976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80772b1b80dc'
down_revision: Union[str, Sequence[str], None] = '387d2b1bfb87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
