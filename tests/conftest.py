import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.core.database import get_db
from app.models import Base, Categories, Product, Stockmovement
from main import APP

load_dotenv()

database_url = os.getenv("TEST_DATABASE_URL")
if not database_url:
    raise RuntimeError("Configure TEST_DATABASE_URL no arquivo .env")

test_url = make_url(database_url)
if test_url.database != "product_manager_test":
    raise RuntimeError("Os testes só podem usar o banco product_manager_test")

TEST_DATABASE_URL = test_url.set(drivername="postgresql+psycopg").render_as_string(
    hide_password=False
)
test_engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    test_engine.dispose()


def clear_test_data():
    with TestSession() as db:
        db.execute(delete(Stockmovement))
        db.execute(delete(Product))
        db.execute(delete(Categories))
        db.commit()


@pytest.fixture(autouse=True)
def clean_database(create_test_tables):
    clear_test_data()
    yield
    clear_test_data()


@pytest.fixture
def client():
    def override_get_db():
        with TestSession() as db:
            yield db

    APP.dependency_overrides[get_db] = override_get_db
    with TestClient(APP) as test_client:
        yield test_client
    APP.dependency_overrides.pop(get_db, None)
