import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture(scope='session')
def engine():

    db_url = os.getenv('DB_URL')
    if not db_url:
        raise ValueError("A variável de ambiente DB_URL não está definida.")
    return create_engine(db_url)

@pytest.fixture(scope='session')
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture(scope='function')
def db_session(engine, tables):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
