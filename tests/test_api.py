import pytest

from app.redirector import app

add_path = "/add"
go_path = "/go/{}"
delete_path = "/delete/{}"


@pytest.fixture
def client():
    return app.test_client()


def test_add_invalid(client):
    response = client.post(add_path)
    assert response.status_code == 415

    response = client.post(add_path, json={})
    assert response.status_code == 400

    response = client.post(add_path, json=[])
    assert response.status_code == 400

    response = client.post(add_path, json=["target"])
    assert response.status_code == 400

    response = client.post(add_path, json={"target": 1})
    assert response.status_code == 400

    response = client.post(add_path, json={"target": "google"})
    assert response.status_code == 400

    response = client.post(add_path, json={"target": "google."})
    assert response.status_code == 400

    response = client.post(add_path, json={"target": "google.com"})
    assert response.status_code == 400

    response = client.post(add_path, json={"target": "https://google"})
    assert response.status_code == 400

    response = client.post(add_path, json={"target": "https://google."})
    assert response.status_code == 400

    response = client.post(add_path, json={"target": "https://google.c"})
    assert response.status_code == 400


def test_add_with_src(client):
    global defined_src
    defined_src = "a123456789"
    target = "https://google.com"
    response = client.post(add_path, json={"src": defined_src, "target": target})
    assert response.status_code == 200
    assert response.json["src"] == defined_src
    assert response.json["target"] == target


def test_add_with_duplicate_src(client):
    target = "https://test.com"
    response = client.post(add_path, json={"src": defined_src, "target": target})
    assert response.status_code == 400


def test_add(client):
    target = "https://google.com"
    response = client.post(add_path, json={"target": target})
    assert response.status_code == 200
    assert "src" in response.json
    assert response.json["target"] == target

    global src
    src = response.json["src"]


def test_go_no_target(client):
    response = client.get(go_path.format("test"))
    assert response.status_code == 404


def test_go(client):
    response = client.get(go_path.format(src))
    assert response.status_code == 302


def test_delete_no_target(client):
    response = client.delete(delete_path.format("test"))
    assert response.status_code == 404


def test_delete(client):
    response = client.delete(delete_path.format(defined_src))
    assert response.status_code == 200

    response = client.delete(delete_path.format(src))
    assert response.status_code == 200
