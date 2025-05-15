import os
from dagster import EnvVar
from dagster_duckdb import DuckDBResource
from dagster_duckdb_polars import DuckDBPolarsIOManager

duckdb_resource = DuckDBResource(
    database=EnvVar("DATABASE_PATH")
)
io_manager = DuckDBPolarsIOManager(database=EnvVar("DATABASE_PATH"), schema="main")
