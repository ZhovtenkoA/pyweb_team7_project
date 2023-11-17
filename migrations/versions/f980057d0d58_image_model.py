"""image model

Revision ID: f980057d0d58
Revises: 6c193e39c7e1
Create Date: 2023-11-15 23:46:23.402238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f980057d0d58'
down_revision: Union[str, None] = '6c193e39c7e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
