"""Creates table

Revision ID: f343eb3aed7d
Revises: b42ff25560ab
Create Date: 2024-10-27 22:20:48.116282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f343eb3aed7d'
down_revision = 'b42ff25560ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_input', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_profile_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(None, 'user_profile', ['user_profile_id'], ['id'])

    with op.batch_alter_table('user_profile', schema=None) as batch_op:
        batch_op.drop_column('user_input_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_profile', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_input_id', sa.INTEGER(), nullable=True))

    with op.batch_alter_table('user_input', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('user_profile_id')

    # ### end Alembic commands ###
