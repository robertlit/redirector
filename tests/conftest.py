import pytest

from app.data import RedisDataStore
from app.redirector import create_app


@pytest.fixture
def data_store():
    data_store = RedisDataStore(decode_responses=True)

    yield data_store

    data_store.r.flushdb()


@pytest.fixture
def app(data_store):
    return create_app(data_store)


@pytest.fixture
def client(app):
    return app.test_client()
