"""add_archive_table_function

Revision ID: 18521fbc0a3c
Revises: 469627e28100
Create Date: 2024-05-26 00:47:03.459229

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '18521fbc0a3c'
down_revision: Union[str, None] = '469627e28100'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """pure sql trigger-based archival
    https://www.thegnar.com/blog/history-tracking-with-postgres
    """
    CREATE_TABLE = """\
CREATE TABLE IF NOT EXISTS archives (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    record_type TEXT NOT NULL,
    record_id UUID NOT NULL,
    operation TEXT NOT NULL,
    old_values JSONB,
    new_values JSONB,
    most_recent BOOLEAN NOT NULL DEFAULT TRUE,
    recorded_at TIMESTAMP NOT NULL
    );"""

    CREATE_FUNCTION = """\
CREATE FUNCTION make_archive_of_changes() RETURNS TRIGGER AS $$
  -- Expects one argument, the record_type
  -- It's the stringified ActiveRecord class name
  -- For example 'User', or 'Account'
  BEGIN
    -- Previous snapshots should be marked as stale
    -- This little denormalization trick is so that ~ActiveRecord~ SQLAlchemy
    -- can immediately pull up the most recent snapshot without
    -- having to sort through all the records by their timestamps
    UPDATE archives
    SET most_recent = FALSE
    WHERE
      table_name = TG_TABLE_NAME
      AND most_recent = TRUE
      AND record_type = record_type
      AND record_id = (
        CASE WHEN TG_OP = 'DELETE'
          THEN OLD.uid
          ELSE NEW.uid
        END
      );


    IF TG_OP = 'INSERT' THEN
      INSERT INTO archives (
        table_name, record_type, record_id, operation, new_values, most_recent, recorded_at
      )
      VALUES (
        TG_TABLE_NAME, TG_ARGV[0], NEW.uid, TG_OP, to_jsonb(NEW), TRUE, now()
      );
      RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
      INSERT INTO archives (
        table_name, record_type, record_id, operation, new_values, old_values, most_recent, recorded_at
      )
      VALUES (
        TG_TABLE_NAME, TG_ARGV[0], NEW.uid, TG_OP, to_jsonb(NEW), to_jsonb(OLD), TRUE, now()
      );
      RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
      INSERT INTO archives (
        table_name, record_type, record_id, operation, old_values, most_recent, recorded_at
      )
      VALUES (
        TG_TABLE_NAME, TG_ARGV[0], OLD.uid, TG_OP, to_jsonb(OLD), TRUE, now()
      );
      RETURN OLD;

    END IF;
  END;
$$ language plpgsql;
"""
    for query in (
            CREATE_TABLE,
            CREATE_FUNCTION,
    ):
        op.execute(sa.text(query))


def downgrade() -> None:
    DROP_TABLE = "DROP TABLE IF EXISTS archives;"
    DROP_FUNCTION = "DROP FUNCTION IF EXISTS make_archive_of_changes;"
    for query in (
            DROP_TABLE,
            DROP_FUNCTION,
    ):
        op.execute(sa.text(query))
