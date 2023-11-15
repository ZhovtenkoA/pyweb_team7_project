"""new

Revision ID: 52e7553de8ab
Revises: f980057d0d58
Create Date: 2023-11-16 00:01:24.053044

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52e7553de8ab'
down_revision: Union[str, None] = 'f980057d0d58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
