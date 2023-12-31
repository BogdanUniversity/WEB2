"""initial commit


Revision ID: 41ea852e2f94
Revises: 
Create Date: 2023-11-29 12:17:10.733121

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41ea852e2f94'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=500), nullable=True),
    sa.Column('password', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('following_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('UserID', sa.Integer(), nullable=False),
    sa.Column('FolloweeID', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['FolloweeID'], ['user_table.id'], ),
    sa.ForeignKeyConstraint(['UserID'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_table')
    op.drop_table('following_table')
    op.drop_table('user_table')
    # ### end Alembic commands ###
