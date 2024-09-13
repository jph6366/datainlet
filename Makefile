.DEFAULT_GOAL := run

run:
	uv run dagster-dbt project prepare-and-package --file datalia/dbt_project.py
	uv run dagster asset materialize --select \* -m datalia.definitions

dev:
	dagster dev

setup:
	uv sync
	. .venv/bin/activate

clean:
	rm -rf data/*.parquet data/*.duckdb
	rm -rf dbt/target dbt/dbt_packages dbt/logs
