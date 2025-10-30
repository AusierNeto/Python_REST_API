"""create product_snapshot and favorites table

Revision ID: 387d2b1bfb87
Revises: a84a6e1d9b2e
Create Date: 2025-10-29 23:52:48.336001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '387d2b1bfb87'
down_revision: Union[str, Sequence[str], None] = 'a84a6e1d9b2e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
