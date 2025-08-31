"""add_role_and_is_active_to_users

Revision ID: 96e066a6b6fb
Revises: 9c19878bbb15
Create Date: 2025-08-31 17:21:52.551134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '96e066a6b6fb'
down_revision: Union[str, None] = '9c19878bbb15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    # Drop the index first
    op.drop_index(op.f('ix_users_role'), table_name='users')
    
    # Drop the columns
    op.drop_column('users', 'is_active')
    op.drop_column('users', 'role')
