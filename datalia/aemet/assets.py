import datetime

import dagster as dg
import polars as pl

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
    # duckdb: DuckDBResource,
    aemet_api: AEMETAPI,
    # ) -> dg.MaterializeResult:
) -> pl.DataFrame:
    """
    Datos meteorológicos de AEMET de todas las estaciones meteorológicas en España desde 1920.
    """

    from_date = datetime.datetime(1920, 1, 1).date()
    to_date = datetime.date.today() - datetime.timedelta(days=1)

    context.log.info(f"Getting data from {from_date} to {to_date}")

    df = pl.DataFrame(aemet_api.get_weather_data(from_date, to_date, batch_size=30))

    return df

    # AEMET_API_FIRST_DAY = datetime.datetime(1920, 1, 1).date()
    # asset_name = context.asset_key.to_user_string()

    # with duckdb.get_connection() as conn:
    #     try:
    #         from_date = conn.execute(
    #             f"""
    #             select
    #                 max(fecha)
    #             from 'main.{asset_name}';
    #             """
    #         ).fetchall()[0][0]

    #         from_date = from_date + datetime.timedelta(days=1)
    #     except CatalogException:
    #         from_date = AEMET_API_FIRST_DAY

    # to_date = datetime.date.today() - datetime.timedelta(days=1)

    # context.log.info(f"Data missing range: {from_date} to {to_date}")

    # if from_date >= to_date:
    #     context.log.info("No data to insert")
    #     return dg.MaterializeResult()

    # r = aemet_api.get_weather_data(from_date, to_date)

    # df = pl.DataFrame()
    # for d in r:
    #     ndf = pl.DataFrame(d)
    #     df = pl.concat([df, ndf], how="diagonal_relaxed")

    # if df.shape[0] == 0:
    #     context.log.info("No data to insert")
    #     return dg.MaterializeResult()

    # df = df.with_columns(pl.col("fecha").str.strptime(pl.Date, format="%Y-%m-%d"))

    # float_columns = [
    #     "prec",
    #     "presMax",
    #     "presMin",
    #     "racha",
    #     "sol",
    #     "tmax",
    #     "tmed",
    #     "tmin",
    #     "velmedia",
    # ]

    # df = df.with_columns(
    #     [
    #         pl.col(col).str.replace(",", ".").cast(pl.Float64, strict=False)
    #         for col in float_columns
    #     ]
    # )

    # context.log.info(f"Inserting latest data into main.{asset_name}")

    # with duckdb.get_connection() as conn:
    #     query = f"create or replace table 'main.{asset_name}' as select * from df"

    #     print(from_date, AEMET_API_FIRST_DAY)
    #     if from_date != AEMET_API_FIRST_DAY:
    #         query = query + f" union all select * from 'main.{asset_name}'"

    #     conn.execute(query)

    # return dg.MaterializeResult()
