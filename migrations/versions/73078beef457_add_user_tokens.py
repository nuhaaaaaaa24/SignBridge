"""add user tokens

Revision ID: 73078beef457
Revises: 9f4fb704648e
Create Date: 2026-04-22 22:46:46.255992

"""
from alembic import op
import sqlalchemy as sa


revision = '73078beef457'
down_revision = '9f4fb704648e'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.create_foreign_key('fk_message_user_id', 'user', ['user_id'], ['id'], ondelete='SET NULL')

    with op.batch_alter_table('room_participant', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_rp_user_id', 'user', ['rp_user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_foreign_key('fk_rp_room_id', 'room', ['rp_room_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token', sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column('token_expiration', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_token'), ['token'], unique=True)


def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_token'))
        batch_op.drop_column('token_expiration')
        batch_op.drop_column('token')

    with op.batch_alter_table('room_participant', schema=None) as batch_op:
        batch_op.drop_constraint('fk_rp_user_id', type_='foreignkey')
        batch_op.drop_constraint('fk_rp_room_id', type_='foreignkey')

    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_constraint('fk_message_user_id', type_='foreignkey')
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)