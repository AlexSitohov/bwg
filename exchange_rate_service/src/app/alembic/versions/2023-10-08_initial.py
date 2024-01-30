from alembic import op
import sqlalchemy as sa

revision = "c0f94cf348c4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'exchange_rates',
        sa.Column("id", sa.UUID(as_uuid=False), nullable=False),
        sa.Column('currency_pair_name', sa.String(25), nullable=False),
        sa.Column('price', sa.FLOAT, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),

    )


def downgrade():
    op.drop_table('exchange_rates')
