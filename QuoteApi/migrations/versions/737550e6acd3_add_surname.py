"""Add surname

Revision ID: 737550e6acd3
Revises: 0ddc960cfaf1
Create Date: 2025-06-01 10:20:40.394149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '737550e6acd3'
down_revision = '0ddc960cfaf1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('authors', schema=None) as batch_op:
        batch_op.alter_column('surname',
               existing_type=sa.VARCHAR(length=32),
               nullable=False)
        batch_op.create_index(batch_op.f('ix_authors_surname'), ['surname'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('authors', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_authors_surname'))
        batch_op.alter_column('surname',
               existing_type=sa.VARCHAR(length=32),
               nullable=True)

    # ### end Alembic commands ###
