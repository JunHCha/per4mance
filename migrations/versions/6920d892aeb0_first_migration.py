"""first migration

Revision ID: 6920d892aeb0
Revises: 
Create Date: 2021-11-27 22:35:00.503533

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "6920d892aeb0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(), nullable=False),
        sa.Column("name", sa.String(length=30), nullable=True),
        sa.Column("company", sa.String(length=30), nullable=True),
        sa.Column("account", sa.String(length=200), nullable=True),
        sa.Column("password", sa.String(length=200), nullable=True),
        sa.Column("email_address", sa.String(length=200), nullable=True),
        sa.Column("is_evaluator", sa.BOOLEAN(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user")
    # ### end Alembic commands ###
