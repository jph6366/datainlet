.DEFAULT_GOAL := run

.PHONY: .uv
.uv:
	@uv -V || echo 'Please install uv: https://docs.astral.sh/uv/getting-started/installation/'

.PHONY: setup
setup: .uv
	uv sync --frozen --all-groups

db:
	wget https://github.com/davidgasquez/datania/releases/latest/download/datania.duckdb -O data/database.duckdb

run: .uv
	uv run dagster asset materialize --select \* -m datania.definitions

dev: .uv
	uv run dagster dev

.PHONY: web
web:
	npm run dev --prefix web

clean:
	rm -rf data/*.parquet data/*.duckdb
