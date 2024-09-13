import polars as pl
from dagster import AssetExecutionContext, RetryPolicy, asset
from dagster_dbt import DbtCliResource, dbt_assets

from .dbt_project import dbt_project


@dbt_assets(manifest=dbt_project.manifest_path)
def dbt(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()


@asset(
    retry_policy=RetryPolicy(max_retries=5),
)
def raw_ipc() -> pl.DataFrame:
    """
    Datos de la serie histórica del Índice de Precios de Consumo (IPC) en España en formato CSV.
    """

    df = pl.read_csv(
        "https://www.ine.es/jaxiT3/files/t/csv_bdsc/50904.csv", separator=";"
    )

    return df
