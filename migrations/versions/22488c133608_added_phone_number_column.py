"""added phone number column

Revision ID: 22488c133608
Revises: 66e43f7a091b
Create Date: 2022-07-18 15:02:02.268054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22488c133608'
down_revision = '66e43f7a091b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone', sa.String(length=20), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone')
    # ### end Alembic commands ###
