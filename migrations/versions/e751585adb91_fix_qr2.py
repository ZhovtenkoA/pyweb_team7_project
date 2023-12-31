"""fix qr2

Revision ID: e751585adb91
Revises: 994724d78db1
Create Date: 2023-11-15 14:12:06.854524

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e751585adb91"
down_revision: Union[str, None] = "994724d78db1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "qr_codes",
        "url",
        existing_type=sa.VARCHAR(length=255),
        type_=sa.String(length=250),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "qr_codes",
        "url",
        existing_type=sa.String(length=250),
        type_=sa.VARCHAR(length=255),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
