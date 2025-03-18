"""add role column

Revision ID: 002
Revises: 001
Create Date: 2025-03-18 13:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('role', sa.String(length=50), nullable=False, server_default='user'))


def downgrade() -> None:
    op.drop_column('users', 'role')
