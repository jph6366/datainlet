import os

from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource
from dagster_duckdb_polars import DuckDBPolarsIOManager

from . import assets, dbt_project

DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/database.duckdb")

all_assets = load_assets_from_modules([assets])

resources = {
    "io_manager": DuckDBPolarsIOManager(database=DATABASE_PATH, schema="raw"),
    "dbt": DbtCliResource(project_dir=dbt_project.dbt_project),
}

defs = Definitions(assets=all_assets, resources=resources)
