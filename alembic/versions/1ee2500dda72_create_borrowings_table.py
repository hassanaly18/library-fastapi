"""create borrowings table

Revision ID: 1ee2500dda72
Revises: d0c893c96cab
Create Date: 2026-09-13 15:05:32.533870

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '1ee2500dda72'
down_revision: Union[str, Sequence[str], None] = 'd0c893c96cab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # The borrowings table already exists in the database.
    # No changes are required.
    pass


def downgrade() -> None:
    """Downgrade schema."""

    # This migration did not create the table in the current
    # database state, so we don't remove it here.
    pass
