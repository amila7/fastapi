"""add foriegn-key table

Revision ID: c0991f75ef93
Revises: 4e1946557c25
Create Date: 2025-02-03 17:19:01.557756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0991f75ef93'
down_revision: Union[str, None] = '4e1946557c25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'post_users_fk', 
        source_table="posts", 
        referent_table="users",
        local_cols=['owner_id'], 
        remote_cols=['id'], 
        ondelete="CASCADE"
    )
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
