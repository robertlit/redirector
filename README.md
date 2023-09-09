# Redirector
A simple URL shortener implemented with Flask and Redis

# Running
Create a [virtual environment](https://docs.python.org/3/tutorial/venv.html), then run
```commandline
pip install -r requirements.txt
python run.py
```

# Testing
```commandline
pytest
```

# Data Storage
Both in-memory and Redis data storage are implemented and can be used interchangeably

# Endpoints

## POST /add
Adds a redirect
<details>
<summary>Request schema</summary>

```json
{
  "type": "object",
  "properties": {
    "src": {
      "type": "string"
    },
    "target": {
      "type": "string",
      "format": "uri"
    }
  },
  "required": ["target"]
}
```
`src` must not already have an associated target
</details>

<details>
<summary>Response schema</summary>

```json
{
  "type": "object",
  "properties": {
    "status": {
      "type": "string"
    },
    "src": {
      "type": "string"
    },
    "target": {
      "type": "string",
      "format": "uri"
    }
  },
  "required": ["status", "src", "target"]
}
```
</details>

## GET /go/{src}
Redirects to the target associated with src, if exists

## DELETE /delete/{src}
Deletes a redirect, if exists