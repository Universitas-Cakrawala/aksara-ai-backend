"""Initial migration - create user tables

Revision ID: 001_initial
Revises:
Create Date: 2025-09-10 10:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create user table
    op.create_table(
        "user",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("deleted", sa.Boolean(), nullable=False, default=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_by", sa.String(), nullable=False),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)

    # Create user_profile table
    op.create_table(
        "user_profile",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("id_user", sa.String(), nullable=False),
        sa.Column("nama_lengkap", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("tipe_akun", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("deleted", sa.Boolean(), nullable=False, default=False),
        sa.Column("created_by", sa.String(), nullable=False),
        sa.Column("created_date", sa.DateTime(), nullable=True),
        sa.Column("updated_by", sa.String(), nullable=False),
        sa.Column("updated_date", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_user"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_profile_id"), "user_profile", ["id"], unique=False)
    op.create_index(
        op.f("ix_user_profile_id_user"), "user_profile", ["id_user"], unique=True
    )


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index(op.f("ix_user_profile_id_user"), table_name="user_profile")
    op.drop_index(op.f("ix_user_profile_id"), table_name="user_profile")
    op.drop_table("user_profile")

    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_table("user")
