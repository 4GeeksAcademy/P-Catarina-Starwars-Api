"""empty message

Revision ID: ba5c5c10cb4c
Revises: a5cffa318ac2
Create Date: 2024-04-28 17:58:41.977963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba5c5c10cb4c'
down_revision = 'a5cffa318ac2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('people',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('birth_year', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('planets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=False),
    sa.Column('climate', sa.String(length=100), nullable=False),
    sa.Column('terrain', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=True),
    sa.Column('id_fav_person', sa.Integer(), nullable=True),
    sa.Column('id_fav_planet', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_fav_person'], ['people.id'], ),
    sa.ForeignKeyConstraint(['id_fav_planet'], ['planets.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorites')
    op.drop_table('planets')
    op.drop_table('people')
    # ### end Alembic commands ###