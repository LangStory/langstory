import pytest
from sqlalchemy import text

from app.routers.utilities import get_db_session,_create_engine
from app.models.base import Base

@pytest.fixture
def db_session(request):
    function_ = request.node.name
    engine = _create_engine(database="test_langstory")
    with engine.begin() as connection:
        for statement in (text(f"CREATE SCHEMA IF NOT EXISTS {function_}"),
                      text(f"SET search_path TO {function_},public"),):
            engine.execute(statement)
        Base.metadata.drop_all(bind=connection)
        Base.metadata.create_all(bind=connection)
    yield get_db_session(engine)