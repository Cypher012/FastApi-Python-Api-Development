"""add user table

Revision ID: e38cf605a824
Revises: 3bcb04dbda05
Create Date: 2024-12-24 17:46:39.545372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e38cf605a824'
down_revision: Union[str, None] = '3bcb04dbda05'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
    'users',
    sa.Column('id', sa.Integer, primary_key=True, nullable=False),
    sa.Column('email', sa.String, nullable=False, unique=True),
    sa.Column('password', sa.String, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
)



def downgrade() -> None:
    op.drop_table('users')
