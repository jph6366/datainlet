import os

from dagster_duckdb import DuckDBResource
from dagster_duckdb_polars import DuckDBPolarsIOManager

DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/database.duckdb")

duckdb_resource = DuckDBResource(database=DATABASE_PATH)
io_manager = DuckDBPolarsIOManager(database=DATABASE_PATH, schema="main")
