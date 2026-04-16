"""add alembic migration file which is create phone number and then use the upgrad and downgrad

Revision ID: f5c2d0aa499b
Revises: 45b19571f1c6
Create Date: 2026-04-15 18:08:06.494075

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5c2d0aa499b'
down_revision: Union[str, Sequence[str], None] = '45b19571f1c6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
