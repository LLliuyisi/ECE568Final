"""empty message

Revision ID: 05b19e802b84
Revises: f873b9d42ade
Create Date: 2020-05-02 18:15:50.194473

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '05b19e802b84'
down_revision = 'f873b9d42ade'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('portfolio', sa.Column('userid', sa.String(length=64), nullable=True))
    op.create_index(op.f('ix_portfolio_userid'), 'portfolio', ['userid'], unique=True)
    op.drop_index('ix_portfolio_username', table_name='portfolio')
    op.drop_column('portfolio', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('portfolio', sa.Column('username', mysql.VARCHAR(length=64), nullable=True))
    op.create_index('ix_portfolio_username', 'portfolio', ['username'], unique=True)
    op.drop_index(op.f('ix_portfolio_userid'), table_name='portfolio')
    op.drop_column('portfolio', 'userid')
    # ### end Alembic commands ###
