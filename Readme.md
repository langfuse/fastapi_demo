# Langfuse FastAPI demo

This is a reference integration of the Langfuse Python SDK into a fastapi server.

For more integration details, see the [Python SDK docs](https://langfuse.com/docs/sdk/python)

## Dev setup

- run with `poetry run start`
- Test with `hey -m GET -T 'application/json' -A 'application/json' -c 1 -n 10 http://127.0.0.1:8000/campaign\?prompt\=bayerns` (requires [hey](https://github.com/rakyll/hey)
