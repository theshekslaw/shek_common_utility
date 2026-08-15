UV ?= uv

.PHONY: install sync lint fmt typecheck test build clean

install:
	$(UV) sync --all-extras

sync:
	$(UV) sync

lint:
	$(UV) run ruff check src

fmt:
	$(UV) run ruff format src
	$(UV) run ruff check --fix src

typecheck:
	$(UV) run mypy src

test:
	$(UV) run pytest

check: lint typecheck test

build:
	$(UV) build

clean:
	rm -rf dist build .mypy_cache .ruff_cache .pytest_cache
