import datetime

import dagster as dg
import polars as pl
from dagster_duckdb import DuckDBResource
from duckdb import CatalogException

from datalia.aemet.resources import AEMETAPI


@dg.asset()
def raw_aemet_stations(aemet_api: AEMETAPI) -> pl.DataFrame:
    """
    Datos de las estaciones meteorológicas de AEMET.
    """

    return pl.DataFrame(aemet_api.get_all_stations())


@dg.asset()
def aemet_stations(raw_aemet_stations: pl.DataFrame) -> pl.DataFrame:
    """
    Datos de las estaciones meteorológicas de AEMET procesados.
    """

    raw_aemet_stations.with_columns(
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

    df = raw_aemet_stations.with_columns(
        [
            pl.col("latitud").map_elements(convert_to_decimal).alias("latitud"),
            pl.col("longitud").map_elements(convert_to_decimal).alias("longitud"),
        ]
    )

    return df


@dg.asset()
def raw_aemet_stations_weather(
    context: dg.AssetExecutionContext,
    duckdb: DuckDBResource,
    aemet_api: AEMETAPI,
) -> dg.MaterializeResult:
    """
    Datos meteorológicos de AEMET de todas las estaciones meteorológicas en España desde 1920.
    """

    AEMET_API_FIRST_DAY = datetime.datetime(1920, 1, 1).date()

    asset_name = context.asset_key.to_user_string()

    with duckdb.get_connection() as conn:
        try:
            from_date: datetime.date = conn.execute(
                f"""
                select
                    max(fecha)
                from 'main.{asset_name}';
                """
            ).fetchall()[0][0]

            from_date = from_date + datetime.timedelta(days=1)
        except CatalogException:
            from_date = AEMET_API_FIRST_DAY

    to_date = datetime.date.today() - datetime.timedelta(days=1)

    context.log.info(f"Missing data range: {from_date} to {to_date}")

    if from_date >= to_date:
        context.log.info("Data is up to date")
        return dg.MaterializeResult()

    df = pl.DataFrame(aemet_api.get_weather_data(from_date, to_date))

    context.log.info(f"Inserting latest data into main.{asset_name}")
    context.log.info(f"Data shape: {df.shape}")

    with duckdb.get_connection() as conn:
        query = f"create or replace table 'main.{asset_name}' as select * from df"

        if from_date != AEMET_API_FIRST_DAY:
            query = query + f" union all select * from 'main.{asset_name}'"

        conn.execute(query)

    return dg.MaterializeResult()
