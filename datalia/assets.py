from datetime import datetime

import polars as pl
from dagster import AssetExecutionContext, RetryPolicy, asset
from dagster_dbt import DbtCliResource, dbt_assets

from .dbt_project import dbt_project
from .resources import AEMETAPI


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


@asset()
def raw_spain_aemet_stations(aemet_api: AEMETAPI) -> pl.DataFrame:
    """
    Datos de las estaciones meteorológicas de AEMET.
    """

    df = pl.DataFrame(aemet_api.get_all_stations())
    df.with_columns(pl.col("indsinop").cast(pl.Int32, strict=False).alias("indsinop"))

    # Clean latitud and longitud
    def convert_to_decimal(coord):
        degrees = int(coord[:-1][:2])
        minutes = int(coord[:-1][2:4])
        seconds = int(coord[:-1][4:])
        decimal = degrees + minutes / 60 + seconds / 3600
        if coord[-1] in ["S", "W"]:
            decimal = -decimal
        return decimal

    df = df.with_columns(
        [
            pl.col("latitud").map_elements(convert_to_decimal).alias("latitud"),
            pl.col("longitud").map_elements(convert_to_decimal).alias("longitud"),
        ]
    )

    return df


@asset()
def raw_spain_aemet_weather(
    context: AssetExecutionContext, aemet_api: AEMETAPI
) -> pl.DataFrame:
    """
    Datos meteorológicos de AEMET de todas las estaciones meteorológicas en España desde 1920.
    """

    start_date = datetime(2024, 1, 1)  # TODO: Cambiar a 1920
    end_date = datetime.now()

    r = aemet_api.get_weather_data(start_date, end_date)

    df = pl.DataFrame()
    for d in r:
        ndf = pl.DataFrame(d)
        df = pl.concat([df, ndf], how="diagonal_relaxed")

    df = df.with_columns(pl.col("fecha").str.strptime(pl.Date, format="%Y-%m-%d"))

    float_columns = [
        "prec",
        "presMax",
        "presMin",
        "racha",
        "sol",
        "tmax",
        "tmed",
        "tmin",
        "velmedia",
    ]

    df = df.with_columns(
        [
            pl.col(col).str.replace(",", ".").cast(pl.Float64, strict=False)
            for col in float_columns
        ]
    )

    return df
