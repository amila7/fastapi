"""add content column to posts table

Revision ID: d5c3da25a1b8
Revises: b074d9f3fc69
Create Date: 2025-02-03 16:26:42.147934

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5c3da25a1b8'
down_revision: Union[str, None] = 'b074d9f3fc69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',  sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
