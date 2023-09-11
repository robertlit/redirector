import pytest


@pytest.fixture
def path():
    return "/delete/{}"


def test_delete_no_target(client, path):
    response = client.delete(path.format("a123456789"))
    assert response.status_code == 404


@pytest.fixture
def src(data_store):
    src = "a123456789"
    target = "https://test.com"
    data_store.add_redirect(src, target)

    yield src

    data_store.delete_redirect(src)


def test_delete(client, path, src):
    response = client.delete(path.format(src))
    assert response.status_code == 200
