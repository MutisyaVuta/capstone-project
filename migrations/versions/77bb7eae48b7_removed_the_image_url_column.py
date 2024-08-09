"""removed the image url column

Revision ID: 77bb7eae48b7
Revises: e4f6242b5f90
Create Date: 2024-08-08 16:36:44.974890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77bb7eae48b7'
down_revision = 'e4f6242b5f90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.drop_column('image_url')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_url', sa.VARCHAR(length=120), autoincrement=False, nullable=True))

    # ### end Alembic commands ###
