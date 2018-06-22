"""empty message

Revision ID: 8d231956707c
Revises: 
Create Date: 2018-06-22 20:15:10.870749

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8d231956707c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('tab_config',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('key', sa.String(), nullable=True),
    sa.Column('value', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key')
    )
    op.create_table('tab_materials',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chapter_id', sa.Integer(), nullable=True),
    sa.Column('chapter_name', sa.Unicode(), nullable=True),
    sa.Column('content', sa.Unicode(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tab_materials_chapter_id'), 'tab_materials', ['chapter_id'], unique=True)
    op.create_index(op.f('ix_tab_materials_chapter_name'), 'tab_materials', ['chapter_name'], unique=False)
    op.create_table('wenbai_scriptures',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scripture_display', sa.Unicode(length=16), nullable=True),
    sa.Column('scripture_title', sa.Unicode(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wenbai_scriptures_scripture_display'), 'wenbai_scriptures', ['scripture_display'], unique=False)
    op.create_index(op.f('ix_wenbai_scriptures_scripture_title'), 'wenbai_scriptures', ['scripture_title'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('wenbai_chapters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('scripture_id', sa.Integer(), nullable=True),
    sa.Column('chapter_display', sa.Unicode(length=16), nullable=True),
    sa.Column('chapter__title', sa.Unicode(length=128), nullable=True),
    sa.ForeignKeyConstraint(['scripture_id'], ['wenbai_scriptures.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wenbai_chapters_chapter__title'), 'wenbai_chapters', ['chapter__title'], unique=False)
    op.create_index(op.f('ix_wenbai_chapters_chapter_display'), 'wenbai_chapters', ['chapter_display'], unique=False)
    op.create_table('wenbai_sentences',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('scripture_id', sa.Integer(), nullable=True),
    sa.Column('chapter_id', sa.Integer(), nullable=True),
    sa.Column('section_id', sa.Integer(), nullable=True),
    sa.Column('classic_text', sa.Text(), nullable=True),
    sa.Column('modern_text', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['chapter_id'], ['wenbai_scriptures.id'], ),
    sa.ForeignKeyConstraint(['scripture_id'], ['wenbai_scriptures.id'], ),
    sa.ForeignKeyConstraint(['section_id'], ['wenbai_scriptures.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wenbai_sectons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chapter_id', sa.Integer(), nullable=True),
    sa.Column('section_display', sa.Unicode(length=16), nullable=True),
    sa.Column('section__title', sa.Unicode(length=128), nullable=True),
    sa.ForeignKeyConstraint(['chapter_id'], ['wenbai_chapters.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_wenbai_sectons_section__title'), 'wenbai_sectons', ['section__title'], unique=False)
    op.create_index(op.f('ix_wenbai_sectons_section_display'), 'wenbai_sectons', ['section_display'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_wenbai_sectons_section_display'), table_name='wenbai_sectons')
    op.drop_index(op.f('ix_wenbai_sectons_section__title'), table_name='wenbai_sectons')
    op.drop_table('wenbai_sectons')
    op.drop_table('wenbai_sentences')
    op.drop_index(op.f('ix_wenbai_chapters_chapter_display'), table_name='wenbai_chapters')
    op.drop_index(op.f('ix_wenbai_chapters_chapter__title'), table_name='wenbai_chapters')
    op.drop_table('wenbai_chapters')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_wenbai_scriptures_scripture_title'), table_name='wenbai_scriptures')
    op.drop_index(op.f('ix_wenbai_scriptures_scripture_display'), table_name='wenbai_scriptures')
    op.drop_table('wenbai_scriptures')
    op.drop_index(op.f('ix_tab_materials_chapter_name'), table_name='tab_materials')
    op.drop_index(op.f('ix_tab_materials_chapter_id'), table_name='tab_materials')
    op.drop_table('tab_materials')
    op.drop_table('tab_config')
    op.drop_table('roles')
    # ### end Alembic commands ###
