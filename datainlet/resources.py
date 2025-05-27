from dagster import EnvVar
from dagster_duckdb import DuckDBResource
from dagster_duckdb_polars import DuckDBPolarsIOManager
from dagster_duckdb_pandas import DuckDBPandasIOManager

duckdb_resource = DuckDBResource(
    database=EnvVar("DATABASE_PATH")
)

#io_manager = DuckDBPolarsIOManager(database=EnvVar("DATABASE_PATH"), schema="main")
io_manager = DuckDBPandasIOManager(database=EnvVar("DATABASE_PATH"), schema="main")
