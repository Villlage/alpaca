"""plaid item and plaid account

Revision ID: afb0dc244186
Revises: 6e7ea92b3444
Create Date: 2020-01-19 21:27:26.971499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "afb0dc244186"
down_revision = "6e7ea92b3444"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "plaid_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("item_id", sa.String(length=255), nullable=False),
        sa.Column("access_token", sa.String(length=255), nullable=True),
        sa.Column("institution_id", sa.String(length=50), nullable=False),
        sa.Column("institution_name", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_plaid_items_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_plaid_items")),
        sa.UniqueConstraint(
            "user_id", "institution_id", name=op.f("uq_plaid_items_user_id")
        ),
    )
    op.create_index(
        op.f("ix_plaid_items_item_id"), "plaid_items", ["item_id"], unique=False
    )
    op.create_table(
        "plaid_accounts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("item_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("account_id", sa.String(length=255), nullable=False),
        sa.Column("plaid_type", sa.String(length=255), nullable=False),
        sa.Column("plaid_subtype", sa.String(length=255), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("official_name", sa.String(length=255), nullable=True),
        sa.Column(
            "current_balance", sa.Numeric(decimal_return_scale=2), nullable=False
        ),
        sa.Column("mask", sa.String(length=4), nullable=True),
        sa.ForeignKeyConstraint(
            ["item_id"],
            ["plaid_items.id"],
            name=op.f("fk_plaid_accounts_item_id_plaid_items"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_plaid_accounts_user_id_users")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_plaid_accounts")),
    )
    op.create_index(
        op.f("ix_plaid_accounts_account_id"),
        "plaid_accounts",
        ["account_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_plaid_accounts_item_id"), "plaid_accounts", ["item_id"], unique=False
    )
    op.create_index(
        op.f("ix_plaid_accounts_user_id"), "plaid_accounts", ["user_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_plaid_accounts_user_id"), table_name="plaid_accounts")
    op.drop_index(op.f("ix_plaid_accounts_item_id"), table_name="plaid_accounts")
    op.drop_index(op.f("ix_plaid_accounts_account_id"), table_name="plaid_accounts")
    op.drop_table("plaid_accounts")
    op.drop_index(op.f("ix_plaid_items_item_id"), table_name="plaid_items")
    op.drop_table("plaid_items")
    # ### end Alembic commands ###
