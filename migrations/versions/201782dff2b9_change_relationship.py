"""Change relationship

Revision ID: 201782dff2b9
Revises: a7fae5b2e0f1
Create Date: 2018-02-28 10:56:09.409000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '201782dff2b9'
down_revision = 'a7fae5b2e0f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('businesses', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint(u'businesses_business_id_fkey', 'businesses', type_='foreignkey')
    op.create_foreign_key(None, 'businesses', 'users', ['user_id'], ['id'])
    op.drop_column('businesses', 'business_id')
    op.add_column('reviews', sa.Column('businessId', sa.Integer(), nullable=True))
    op.drop_constraint(u'reviews_business_fkey', 'reviews', type_='foreignkey')
    op.create_foreign_key(None, 'reviews', 'businesses', ['businessId'], ['id'])
    op.drop_column('reviews', 'business')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('business', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'reviews', type_='foreignkey')
    op.create_foreign_key(u'reviews_business_fkey', 'reviews', 'businesses', ['business'], ['id'])
    op.drop_column('reviews', 'businessId')
    op.add_column('businesses', sa.Column('business_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'businesses', type_='foreignkey')
    op.create_foreign_key(u'businesses_business_id_fkey', 'businesses', 'users', ['business_id'], ['id'])
    op.drop_column('businesses', 'user_id')
    # ### end Alembic commands ###
