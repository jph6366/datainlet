.DEFAULT_GOAL := run

.PHONY: .uv
.uv:
	@uv -V || echo 'Please install uv: https://docs.astral.sh/uv/getting-started/installation/'

.PHONY: setup
setup: .uv
	uv sync --frozen --all-groups

db:
	wget https://github.com/jph6366/datainlet/releases/latest/download/datania.duckdb -O data/database.duckdb

run: .uv
	uv run dagster asset materialize --select \* -m datainlet.definitions

dev: .uv
	uv run dagster dev

.PHONY: web
web:
	uv run python -m http.server 8000 --directory web

clean:
	rm -rf data/*.parquet data/*.duckdb
