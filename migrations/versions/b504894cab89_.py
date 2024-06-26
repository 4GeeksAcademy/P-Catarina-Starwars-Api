"""empty message

Revision ID: b504894cab89
Revises: ba5c5c10cb4c
Create Date: 2024-04-28 19:00:13.722821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b504894cab89'
down_revision = 'ba5c5c10cb4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_person', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('id_planet', sa.Integer(), nullable=True))
        batch_op.drop_constraint('favorites_id_fav_person_fkey', type_='foreignkey')
        batch_op.drop_constraint('favorites_id_fav_planet_fkey', type_='foreignkey')
        batch_op.create_foreign_key(None, 'planets', ['id_planet'], ['id'])
        batch_op.create_foreign_key(None, 'people', ['id_person'], ['id'])
        batch_op.drop_column('id_fav_planet')
        batch_op.drop_column('id_fav_person')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_fav_person', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('id_fav_planet', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('favorites_id_fav_planet_fkey', 'planets', ['id_fav_planet'], ['id'])
        batch_op.create_foreign_key('favorites_id_fav_person_fkey', 'people', ['id_fav_person'], ['id'])
        batch_op.drop_column('id_planet')
        batch_op.drop_column('id_person')

    # ### end Alembic commands ###
