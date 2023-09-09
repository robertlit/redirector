import json

from flask import Flask, request, abort, redirect
from werkzeug.exceptions import HTTPException

from app.data import DataStore, MemoryDataStore, RedisDataStore
from app.generation import generate_random_src
from app.validation import validate_request_body

app = Flask(__name__)
# data_store: DataStore = MemoryDataStore()
data_store: DataStore = RedisDataStore(decode_responses=True)


@app.post("/add")
def add_redirect():
    data = request.get_json()

    is_valid, err_msg = validate_request_body(data)
    if not is_valid:
        abort(400, err_msg)

    if "src" in data:
        src = data["src"]
        if data_store.has_redirect(src):
            abort(400, f"Redirect with {src=} already exists")
    else:
        src = generate_random_src()

    target = data["target"]

    data_store.add_redirect(src, target)

    return {
        "status": "ok",
        "src": src,
        "target": target
    }


@app.get("/go/<src>")
def go_to_target(src):
    target = data_store.get_target(src)

    if target is None:
        abort(404, f"No target found for {src}")

    return redirect(target)


@app.delete("/delete/<src>")
def delete_redirect(src):
    deleted = data_store.delete_redirect(src)

    if not deleted:
        abort(404, f"No target found for {src}")

    return {
        "status": "ok"
    }


@app.errorhandler(HTTPException)
def handle_exception(e: HTTPException):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description
    })
    response.content_type = "application/json"
    return response
