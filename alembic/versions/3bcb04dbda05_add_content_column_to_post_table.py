"""add content column to post table

Revision ID: 3bcb04dbda05
Revises: 3e303fd26e5c
Create Date: 2024-12-24 17:42:02.396854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bcb04dbda05'
down_revision: Union[str, None] = '3e303fd26e5c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
