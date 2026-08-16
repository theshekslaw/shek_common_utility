# Architecture — shek_common_utility

## Purpose

Shared Python library consumed by every backend service in the `shek_*` ecosystem as a **git-pinned dependency**. Zero-dependency-at-runtime except structlog, pydantic, pydantic-settings, httpx.

## Non-purposes

- Not a framework. No opinions on what your service does.
- Not a config store. It provides base classes and helpers; the service defines its own settings.
- Not an ORM / DB wrapper. That lives in `shek_brain`.

## Module map

```
src/shek_common_utility/
├─ __init__.py                 re-exports the public surface
├─ logging.py                  configure_logging, get_logger (structlog)
├─ settings.py                 BaseServiceSettings (pydantic-settings)
├─ http.py                     AsyncHTTPClient (httpx wrapper: retries, bearer auth)
├─ model_engine_client.py      typed async client for model_engine
└─ brain_client.py             typed async client for shek_brain
```

## Public API surface (frozen for v0.1.x)

- `configure_logging(service, level, json)` — call once in service startup.
- `get_logger(name, **initial_context)` — bound logger with kwargs as persistent context.
- `BaseServiceSettings` — subclass, add your fields; env + `.env` loading, `AUTH_TOKEN` field standard.
- `AsyncHTTPClient(base_url, auth_token, timeout, default_headers)` — httpx wrapper.
- `ModelEngineClient(base_url, auth_token, timeout)` — `list_tasks`, `run_task`, `health`.
- `BrainClient(base_url, auth_token, timeout)` — `ingest_paper` (v0.1 stub), `semantic_search`, `graph_view`, `get_paper`, `health`. **Signatures will evolve as `shek_brain` firms up its schema-registry API.**

## Release model

Semver, tags pushed to GitHub. Consumers pin by tag:

```toml
"shek-common-utility @ git+ssh://git@github.com/theshekslaw/shek_common_utility.git@v0.1.0"
```

Breaking changes → minor bump pre-1.0, major post-1.0.

## Not-yet-decided

- Whether to publish to a private PyPI. For now, git-pinned works and matches user preference against submodules.
- Whether to add an `otel/` submodule for OpenTelemetry setup. Deferred until we actually need distributed traces.
