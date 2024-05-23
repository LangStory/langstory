from typing import Generator, Optional, TYPE_CHECKING
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine

from app.settings import settings

if TYPE_CHECKING:
    from sqlalchemy.orm import Session




def _create_engine(database:Optional[str]=None)-> Engine:
        database = database or settings.db_name
        return create_engine(URL.create(
            drivername="postgresql",
            host=settings.db_host,
            port=settings.db_port,
            username=settings.db_user,
            password=settings.db_password,
            database=database,
        ))

def get_db_session(engine:Optional[Engine] = None) -> "Generator[Session, None, None]":
    engine = engine or _create_engine()
    bound_session = sessionmaker(bind=engine)
    with bound_session() as session:
        yield session