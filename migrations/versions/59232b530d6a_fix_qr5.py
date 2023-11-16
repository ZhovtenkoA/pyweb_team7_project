"""fix qr5

Revision ID: 59232b530d6a
Revises: 4f1237ffb589
Create Date: 2023-11-15 14:46:51.318497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59232b530d6a'
down_revision: Union[str, None] = '4f1237ffb589'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('qr_images',
    sa.Column('image_id', sa.Integer(), nullable=False),
    sa.Column('qr_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], ),
    sa.ForeignKeyConstraint(['qr_id'], ['qr_codes.id'], ),
    sa.PrimaryKeyConstraint('image_id', 'qr_id')
    )
    op.drop_constraint('images_qr_code_id_fkey', 'images', type_='foreignkey')
    op.drop_column('images', 'qr_code_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('images', sa.Column('qr_code_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('images_qr_code_id_fkey', 'images', 'qr_codes', ['qr_code_id'], ['id'])
    op.drop_table('qr_images')
    # ### end Alembic commands ###
