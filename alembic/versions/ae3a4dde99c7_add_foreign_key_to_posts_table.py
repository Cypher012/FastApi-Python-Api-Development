"""add foreign key to posts table

Revision ID: ae3a4dde99c7
Revises: e38cf605a824
Create Date: 2024-12-24 18:01:13.687337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ae3a4dde99c7'
down_revision: Union[str, None] = 'e38cf605a824'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['user_id'], remote_cols=['id'], ondelete='CASCADE')

def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts', type_='foreignkey')
    op.drop_column('posts', 'user_id')
