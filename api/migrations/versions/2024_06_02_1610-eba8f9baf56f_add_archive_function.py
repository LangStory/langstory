"""add_archive_function

Revision ID: eba8f9baf56f
Revises: 4bb96acf7278
Create Date: 2024-06-02 16:10:31.754234

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = "eba8f9baf56f"
down_revision: Union[str, None] = "4bb96acf7278"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """pure sql trigger-based archival
    https://www.thegnar.com/blog/history-tracking-with-postgres
    """
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
    op.execute(sa.text(CREATE_FUNCTION))


def downgrade() -> None:
    DROP_FUNCTION = "DROP FUNCTION IF EXISTS make_archive_of_changes;"
    op.execute(sa.text(DROP_FUNCTION))
