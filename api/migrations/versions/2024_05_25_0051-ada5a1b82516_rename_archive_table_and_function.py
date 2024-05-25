"""rename_archive_table_and_function

Revision ID: ada5a1b82516
Revises: fa55aa15c505
Create Date: 2024-05-25 00:51:20.687485

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'ada5a1b82516'
down_revision: Union[str, None] = 'fa55aa15c505'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename the id column to uid in the archives table
    op.execute("ALTER TABLE archives RENAME COLUMN id TO uid;")

    # Update the make_archive_of_changes function to use 'uid' instead of '_id'
    UPDATE_FUNCTION = """\
CREATE OR REPLACE FUNCTION make_archive_of_changes() RETURNS TRIGGER AS $$
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
      AND record_type = TG_ARGV[0]
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
    op.execute(sa.text(UPDATE_FUNCTION))


def downgrade() -> None:
    # Revert the column name change if needed
    op.execute("ALTER TABLE archives RENAME COLUMN uid TO id;")

    # Revert to the previous version of the function if needed
    UPDATE_FUNCTION = """\
CREATE OR REPLACE FUNCTION make_archive_of_changes() RETURNS TRIGGER AS $$
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
      AND record_type = TG_ARGV[0]
      AND record_id = (
        CASE WHEN TG_OP = 'DELETE'
          THEN OLD._id
          ELSE NEW._id
        END
      );

    IF TG_OP = 'INSERT' THEN
      INSERT INTO archives (
        table_name, record_type, record_id, operation, new_values, most_recent, recorded_at
      )
      VALUES (
        TG_TABLE_NAME, TG_ARGV[0], NEW._id, TG_OP, to_jsonb(NEW), TRUE, now()
      );
      RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
      INSERT INTO archives (
        table_name, record_type, record_id, operation, new_values, old_values, most_recent, recorded_at
      )
      VALUES (
        TG_TABLE_NAME, TG_ARGV[0], NEW._id, TG_OP, to_jsonb(NEW), to_jsonb(OLD), TRUE, now()
      );
      RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
      INSERT INTO archives (
        table_name, record_type, record_id, operation, old_values, most_recent, recorded_at
      )
      VALUES (
        TG_TABLE_NAME, TG_ARGV[0], OLD._id, TG_OP, to_jsonb(OLD), TRUE, now()
      );
      RETURN OLD;

    END IF;
  END;
$$ language plpgsql;
"""
    op.execute(sa.text(UPDATE_FUNCTION))
