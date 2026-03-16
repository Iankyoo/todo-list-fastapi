from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine, event
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry
from fast_zero.security import get_password_hash


@pytest.fixture
def client(session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(bind=engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(bind=engine)
    engine.dispose()


@contextmanager
def _mock_db_time(*, model, time=None):
    if time is None:
        time = datetime.now()

    def hook_time_db(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time

    event.listen(model, 'before_insert', hook_time_db)

    yield time

    event.remove(model, 'before_insert', hook_time_db)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session: Session):
    password = 'testtest'
    user = User(
        username='Ian',
        email='contato.iankyoo@gmail.com',
        password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']
