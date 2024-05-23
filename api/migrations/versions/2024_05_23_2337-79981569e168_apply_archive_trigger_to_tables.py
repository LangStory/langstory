"""apply_archive_trigger_to_tables

Revision ID: 79981569e168
Revises: 6af019cd07cc
Create Date: 2024-05-23 23:37:02.522711

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '79981569e168'
down_revision: Union[str, None] = '6af019cd07cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

models = (
    ("user", "User"),
    ("organization", "Organization"),
    ("chat", "Chat"),
    ("project", "Project"),
    ("persona", "Persona"),
    ("tool", "Tool"),
    ("systemmessage", "SystemMessage"),
    ("assistantmessage", "AssistantMessage"),
    ("usermessage", "UserMessage"),
    ("toolmessage", "ToolMessage"),
    ("externalevent", "ExternalEvent"),
)


def upgrade() -> None:
    for table, class_name in models:
        statement = f"""\
CREATE OR REPLACE TRIGGER trg_make_archive_of_changes_for_{table}
AFTER INSERT OR DELETE OR UPDATE ON "{table}"
FOR EACH ROW EXECUTE FUNCTION make_archive_of_changes('{class_name}');
"""
        op.execute(sa.text(statement))


def downgrade() -> None:
    for table, _ in models:
        statement = f'DROP TRIGGER IF EXISTS trg_make_archive_of_changes_for_{table} ON "{table}" CASCADE;'
        op.execute(sa.text(statement))
