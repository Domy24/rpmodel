"""migration

Revision ID: 79e19b4ee14a
Revises: d9052dff9815
Create Date: 2025-03-05 00:14:20.959666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy


# revision identifiers, used by Alembic.
revision: str = '79e19b4ee14a'
down_revision: Union[str, None] = 'd9052dff9815'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vehicle', sa.Column('mu_r', sa.Float(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vehicle', 'mu_r')
    # ### end Alembic commands ###
