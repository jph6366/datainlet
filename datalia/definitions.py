import os

from dagster import Definitions, EnvVar, load_assets_from_modules
from dagster_dbt import DbtCliResource
from dagster_duckdb_polars import DuckDBPolarsIOManager

from . import assets, dbt_project, publishing
from .resources import AEMETAPI, DatasetPublisher

DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/database.duckdb")

all_assets = load_assets_from_modules([assets, publishing])

resources = {
    "io_manager": DuckDBPolarsIOManager(database=DATABASE_PATH, schema="main"),
    "dbt": DbtCliResource(project_dir=dbt_project.dbt_project),
    "dp": DatasetPublisher(hf_token=EnvVar("HUGGINGFACE_TOKEN")),
    "aemet_api": AEMETAPI(token=EnvVar("AEMET_API_TOKEN")),
}

defs = Definitions(assets=[*all_assets], resources=resources)
