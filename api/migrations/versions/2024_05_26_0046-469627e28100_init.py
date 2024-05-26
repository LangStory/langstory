"""init

Revision ID: 469627e28100
Revises: 
Create Date: 2024-05-26 00:46:37.204834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '469627e28100'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('archives',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('table_name', sa.TEXT(), nullable=False),
    sa.Column('record_type', sa.TEXT(), nullable=False),
    sa.Column('record_id', sa.UUID(), nullable=False),
    sa.Column('operation', sa.TEXT(), nullable=False),
    sa.Column('old_values', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('new_values', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('most_recent', sa.BOOLEAN(), nullable=False),
    sa.Column('recorded_at', postgresql.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization',
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email_domain', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('avatar_url', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('user',
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('email_address', sa.String(), nullable=True),
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('avatar_url', sa.String(), nullable=True),
    sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('email_address')
    )
    op.create_table('magiclink',
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('token_hash', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('expiration', sa.DateTime(), nullable=False),
    sa.Column('user_uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_uid'], ['user.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('organizationsusers',
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('organization_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.uid'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('project',
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('avatar_url', sa.String(), nullable=True),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('organization_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('chat',
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('project_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('persona',
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('project_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('avatar_url', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['project.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('tool',
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('json_schema', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('project_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['project_id'], ['project.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('assistantmessage',
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('chat_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('role', sa.Enum('user', 'system', 'assistant', 'tool', name='messagerole'), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('externalevent',
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('chat_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('systemmessage',
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('chat_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('role', sa.Enum('user', 'system', 'assistant', 'tool', name='messagerole'), nullable=False),
    sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('usermessage',
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('chat_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('role', sa.Enum('user', 'system', 'assistant', 'tool', name='messagerole'), nullable=False),
    sa.Column('persona_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.uid'], ),
    sa.ForeignKeyConstraint(['persona_id'], ['persona.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    op.create_table('toolcall',
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('request_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('arguments', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('tool_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('assistant_message_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.ForeignKeyConstraint(['assistant_message_id'], ['assistantmessage.uid'], ),
    sa.ForeignKeyConstraint(['tool_id'], ['tool.uid'], ),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('request_id')
    )
    op.create_table('toolmessage',
    sa.Column('uid', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('chat_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('role', sa.Enum('user', 'system', 'assistant', 'tool', name='messagerole'), nullable=False),
    sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('tool_call_request_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
    sa.ForeignKeyConstraint(['chat_id'], ['chat.uid'], ),
    sa.ForeignKeyConstraint(['tool_call_request_id'], ['toolcall.request_id'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('toolmessage')
    op.drop_table('toolcall')
    op.drop_table('usermessage')
    op.drop_table('systemmessage')
    op.drop_table('externalevent')
    op.drop_table('assistantmessage')
    op.drop_table('tool')
    op.drop_table('persona')
    op.drop_table('chat')
    op.drop_table('project')
    op.drop_table('organizationsusers')
    op.drop_table('magiclink')
    op.drop_table('user')
    op.drop_table('organization')
    op.drop_table('archives')
    # ### end Alembic commands ###