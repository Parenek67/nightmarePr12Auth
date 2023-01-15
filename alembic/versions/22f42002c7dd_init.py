"""init

Revision ID: 22f42002c7dd
Revises: 
Create Date: 2023-01-06 15:39:31.206335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22f42002c7dd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id',sa.Integer, primary_key=True, index=True),
        sa.Column('name',sa.String),
        sa.Column('login',sa.String),
        sa.Column('password',sa.String)
    )


def downgrade():
    op.drop_table('users')
