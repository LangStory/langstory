"""add_archive_fn_to_models

Revision ID: 57bddb58b53d
Revises: eba8f9baf56f
Create Date: 2024-06-02 16:12:54.203356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '57bddb58b53d'
down_revision: Union[str, None] = 'eba8f9baf56f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


models = (
    ("user", "User"),
    ("organization", "Organization"),
    ("chat", "Chat"),
    ("project", "Project"),
    ("persona", "Persona"),
    ("tool", "Tool"),
    ("message", "Message"),
    ("tool_call", "ToolCall"),
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