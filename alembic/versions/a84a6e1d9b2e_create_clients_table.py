"""create clients table

Revision ID: a84a6e1d9b2e
Revises: 7f5159dbafe4
Create Date: 2025-10-29 22:12:39.784731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a84a6e1d9b2e'
down_revision: Union[str, Sequence[str], None] = '7f5159dbafe4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
