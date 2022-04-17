"""merging two heads
Revision ID: 89595ff494bb
Revises: c48cf453b00a, f1463e8c5244
Create Date: 2022-04-17 07:27:18.739215
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89595ff494bb'
down_revision = ('c48cf453b00a', 'f1463e8c5244')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass