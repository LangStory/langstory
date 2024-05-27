from typing import Generator, TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class DatabaseMixin:
    """common utilites"""

    db_session: "Generator[Session, None, None]"

    def __init__(self, db_session: "Generator[Session, None, None]"):
        self.db_session = db_session
