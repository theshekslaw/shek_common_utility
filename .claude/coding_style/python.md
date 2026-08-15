# Python coding style — shek_* services

Canonical style for every Python repo in the `shek_*` ecosystem. Other Python repos
should link to this file rather than duplicate.

## Non-negotiables

- **Python 3.12+** — no earlier.
- **uv** for package + venv + Python management. Never `pip install` outside `uv`.
- **Type hints everywhere.** `mypy --strict` must pass on every PR.
- **ruff** for lint + format. Config lives in each repo's `pyproject.toml` under
  `[tool.ruff]`. Rules: `E`, `F`, `I`, `N`, `UP`, `B`, `SIM`, `RUF`.
- **structlog + `configure_logging` from `shek_common_utility`.** No `print()`, no
  ad-hoc `logging.getLogger(...)`.
- **pydantic v2** for all data validation and DTOs. Never hand-roll dict schemas
  for API boundaries.
- **pydantic-settings** (`BaseServiceSettings` from `shek_common_utility`) for env
  config. No `os.getenv(...)` scattered through code.
- **Async-first.** FastAPI routes, DB clients, HTTP calls — all async. If you
  need a sync operation, wrap it in `anyio.to_thread.run_sync`.

## Line length + formatting

- Line length **100**. Matches ruff config.
- Format on save. `make fmt` before every commit.

## Imports

- Absolute imports only inside a package (e.g., `from shek_brain.db.postgres import ...`).
- Standard library → third party → first party, separated by blank lines
  (ruff isort handles this).
- No wildcard imports.

## Naming

- Modules: `snake_case.py`.
- Classes: `PascalCase`.
- Functions + variables: `snake_case`.
- Constants: `UPPER_SNAKE_CASE`.
- Pydantic models: `PascalCase`, suffix with role — `PaperIn`, `PaperOut`,
  `SummarizeRequest`, `SummarizeResponse`. Avoid bare `Paper`.

## Error handling

- Raise the narrowest exception that fits. Prefer a small custom exception
  hierarchy per service (`class BrainError(Exception): ...`, `class NotFound(BrainError): ...`).
- **Never** catch bare `Exception` unless you're at a top-level boundary
  (FastAPI exception handler, Temporal activity wrapper).
- Log errors with structured context (`logger.error("event", paper_id=..., err=str(e))`).
  Don't log-and-re-raise unless the outer layer needs context.
- Fail loud in dev, degrade gracefully at API boundaries in prod (return 4xx/5xx
  with a machine-readable error code).

## FastAPI conventions

- One router per resource, mounted under a versioned prefix (`/v1/papers`).
- Request/response models are pydantic — `response_model=` on every route.
- Dependency injection over global state (`Depends(get_brain_client)`).
- Bearer auth via a `verify_token` dependency in every service; token comes from
  `BaseServiceSettings.auth_token`.

## Tests

- `pytest` + `pytest-asyncio`. `asyncio_mode = "auto"`.
- Every service has `tests/unit/` and `tests/integration/`. Unit tests never
  touch the network or filesystem outside `tmp_path`.
- Integration tests use `testcontainers-python` when they need real DBs; skip if
  Docker isn't available.
- Aim for coverage on **business logic**, not glue. Don't test pydantic models.

## Async DB clients

- One pool per process, initialized in FastAPI's `lifespan`.
- Never open a new connection per request.
- All DB code inside a service lives under `src/<service>/db/`, one module per
  backing store (postgres, mongo, qdrant, neo4j).

## Comments

- Comments are for the *why*, not the *what*. If a function needs a block
  comment to explain what it does, it needs a better name.
- No TODO/FIXME without a linked ticket or dated context.

## Commit hygiene

- Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.
- Small commits > big commits. Each commit should leave the repo green.

## Reusing this style

Every other Python `shek_*` repo should include this file at
`.claude/coding_style/python.md` — either by symlink, git submodule, or a
one-line pointer:

```markdown
# Python style
See https://github.com/theshekslaw/shek_common_utility/blob/main/.claude/coding_style/python.md
```
