import pytest


@pytest.fixture
def path():
    return "/add"


def test_add_no_json_body(client, path):
    response = client.post(path)
    assert response.status_code == 415


@pytest.mark.parametrize("invalid_redirect", [
    {},
    [],
    ["target"],
    {"key": "val"},
    {"target": 1},
    {"target": "google"},
    {"target": "google."},
    {"target": "google.com"},
    {"target": "https://google"},
    {"target": "https://google."},
    {"target": "https://google.c"},
])
def test_add_invalid(client, path, invalid_redirect):
    response = client.post(path, json=invalid_redirect)
    assert response.status_code == 400, str(invalid_redirect)


@pytest.mark.parametrize("redirect", [{"src": "a123456789", "target": "https://test.com"}])
def test_add_with_src(client, path, redirect):
    response = client.post(path, json=redirect)
    assert response.status_code == 200
    assert response.json["src"] == redirect["src"]
    assert response.json["target"] == redirect["target"]


@pytest.fixture
def duplicate_redirect(data_store):
    src = "a123456789"
    target = "https://test.com"
    redirect = {"src": src, "target": target}

    data_store.add_redirect(src, target)

    yield redirect

    data_store.delete_redirect(src)


def test_add_with_duplicate_src(client, path, duplicate_redirect):
    response = client.post(path, json=duplicate_redirect)
    assert response.status_code == 400


@pytest.mark.parametrize("redirect", [{"target": "https://test.com"}])
def test_add(client, path, redirect):
    response = client.post(path, json=redirect)
    assert response.status_code == 200
    assert "src" in response.json
    assert response.json["target"] == redirect["target"]
