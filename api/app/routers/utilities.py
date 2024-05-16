from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import settings


def get_db_session():
    return sessionmaker(bind=create_engine(host=settings.db_host, port=settings.db_port, user=settings.db_user, password=settings.db_password, database=settings.db_name))