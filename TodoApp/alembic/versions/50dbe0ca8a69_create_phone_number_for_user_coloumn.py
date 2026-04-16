"""Create phone number for user coloumn

Revision ID: 50dbe0ca8a69
Revises: f5c2d0aa499b
Create Date: 2026-04-16 10:12:58.895136

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50dbe0ca8a69'
down_revision: Union[str, Sequence[str], None] = 'f5c2d0aa499b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
