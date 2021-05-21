"""Initial schema (Message)

Revision ID: ddb5d89292c1
Revises:
Create Date: 2021-05-22 00:39:40.703004

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'ddb5d89292c1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_message_id'), 'message', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_message_id'), table_name='message')
    op.drop_table('message')
    # ### end Alembic commands ###
