import datetime

import dagster as dg
import polars as pl
from dagster_duckdb import DuckDBResource
from duckdb import CatalogException

from datania.aemet.resources import AEMETAPI


@dg.asset()
def raw_estaciones_aemet(aemet_api: AEMETAPI) -> pl.DataFrame:
    """
    Datos de las estaciones meteorológicas de AEMET.
    """

    return pl.DataFrame(aemet_api.get_all_stations())


@dg.asset()
def estaciones_aemet(raw_estaciones_aemet: pl.DataFrame) -> pl.DataFrame:
    """
    Datos de las estaciones meteorológicas de AEMET procesados.
    """

    df = raw_estaciones_aemet.with_columns(
        pl.col("indsinop").cast(pl.Int32, strict=False).alias("indsinop")
    )

    # Clean latitud and longitud
    def convert_to_decimal(coord):
        degrees = int(coord[:-1][:2])
        minutes = int(coord[:-1][2:4])
        seconds = int(coord[:-1][4:])
        decimal = degrees + minutes / 60 + seconds / 3600
        if coord[-1] in ["S", "W"]:
            decimal = -decimal
        return decimal

    df = raw_estaciones_aemet.with_columns(
        [
            pl.col("latitud").map_elements(convert_to_decimal).alias("latitud"),
            pl.col("longitud").map_elements(convert_to_decimal).alias("longitud"),
        ]
    )

    return df


@dg.asset()
def raw_datos_meteorologicos_estaciones_aemet(
    context: dg.AssetExecutionContext,
    duckdb: DuckDBResource,
    aemet_api: AEMETAPI,
) -> pl.DataFrame:
    """
    Datos meteorológicos de AEMET de todas las estaciones meteorológicas en España desde 1920.
    """

    AEMET_API_FIRST_DAY = datetime.datetime(1920, 1, 1).date()

    with duckdb.get_connection() as conn:
        try:
            df = conn.execute(
                """
                select
                    *
                from 'https://huggingface.co/datasets/datania/datos_meteorologicos_estaciones_aemet/resolve/main/data/datos_meteorologicos_estaciones_aemet.parquet';
                """
            ).pl()
            from_date = df.select(pl.col("fecha").max()).to_series().to_list()[0]
        except CatalogException:
            from_date = AEMET_API_FIRST_DAY

    to_date = datetime.date.today() - datetime.timedelta(days=1)

    context.log.info(f"Missing data range: {from_date} to {to_date}")

    if from_date >= to_date:
        context.log.info("Data is up to date")
        return df

    updated_df = pl.DataFrame(aemet_api.get_weather_data(from_date, to_date))

    updated_df = updated_df.with_columns(pl.col("fecha").str.to_date().alias("fecha"))

    return pl.concat([df, updated_df], how="diagonal_relaxed")


@dg.asset()
def datos_meteorologicos_estaciones_aemet(
    raw_datos_meteorologicos_estaciones_aemet: pl.DataFrame,
) -> pl.DataFrame:
    """
    Datos meteorológicos de AEMET de todas las estaciones meteorológicas en España desde 1920.
    """

    return raw_datos_meteorologicos_estaciones_aemet.with_columns(
        pl.col("altitud").cast(pl.Int32, strict=False).alias("altitud")
    )
