# shek_common_utility

Shared Python utilities for the `shek_*` service ecosystem.

## What's inside

- `logging` — structlog config (JSON in prod, colored console in dev)
- `settings` — pydantic-settings `BaseServiceSettings` base class
- `http` — `AsyncHTTPClient` (httpx wrapper with retries + bearer auth)
- `model_engine_client` — typed async client for the `model_engine` LLM gateway
- `brain_client` — typed async client for `shek_brain` (knowledge store)

## Install (as a git dep in another service)

`pyproject.toml`:

```toml
[project]
dependencies = [
  "shek-common-utility @ git+ssh://git@github.com/theshekslaw/shek_common_utility.git@v0.1.0",
]
```

Then `uv sync`.

## Local dev

```bash
make install
make check    # lint + typecheck + test
```

Requires Python 3.12 (`uv python install 3.12`).
