import pytest
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from app.routers.utilities import _create_engine
from app.app import app
from app.routers.utilities import get_db_session
from app.models.all import Base


@pytest.fixture
def db_session(request):
    function_ = request.node.name
    engine = _create_engine(database="langstory_test")
    with engine.begin() as connection:
        for statement in (
            text(f"CREATE SCHEMA IF NOT EXISTS {function_}"),
            text(f"SET search_path TO {function_},public"),
        ):
            connection.execute(statement)
        Base.metadata.drop_all(bind=connection)
        Base.metadata.create_all(bind=connection)
    with sessionmaker(bind=engine)() as session:
        yield session


@pytest.fixture
def override_get_db(db_session):
    yield db_session


@pytest.fixture
def override_app(override_get_db):
    app.dependency_overrides[get_db_session] = lambda: override_get_db
    return app
