import pytest
import os

from fastapi.testclient import TestClient
from main import app
from tests.seed_database import seed_database
from tests.db_session import TestingSessionLocal, engine
from database.base import Base
from dependencies.session_dependencies import get_session
from models import *

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

    yield

    engine.dispose()

    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture(autouse=True)
def clean_tables():
    db = TestingSessionLocal()
    seed_database(db)

    yield

    db.query(OrderProduct).delete()
    db.query(Order).delete()
    db.query(Product).delete()
    db.query(User).delete()

    db.commit()
    db.close()


def override_get_session():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)