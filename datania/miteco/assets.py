from datetime import datetime

import dagster as dg
import polars as pl

from datania.miteco.resources import MITECOArcGisAPI


@dg.asset()
def raw_embalses(
    context: dg.AssetExecutionContext, miteco_api: MITECOArcGisAPI
) -> pl.DataFrame:
    """
    Datos de los embalses de España desde 1988.

    Datos obtenidos del servidor ArcGIS alojado por el MITECO (Ministerio para la Transición Ecológica y el Reto Demográfico).

    Los datos también están disponibles en este sitio web:
    https://www.miteco.gob.es/es/agua/temas/evaluacion-de-los-recursos-hidricos/boletin-hidrologico.html
    """
    start_year = 1988
    current_year = datetime.now().year

    df = pl.DataFrame()

    for year in range(start_year, current_year + 1):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        context.log.info(
            f"Getting data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
        )
        response = miteco_api.get_water_reservoirs_data(start_date, end_date)
        if response["features"]:
            mdf = pl.from_records(
                [elem["attributes"] for elem in response["features"]],
                infer_schema_length=None,
            )
            df = pl.concat([df, mdf], how="diagonal_relaxed")

    df = df.with_columns(pl.col("fecha").cast(pl.Datetime("ms")))

    return df


@dg.asset()
def embalses(raw_embalses: pl.DataFrame) -> pl.DataFrame:
    """
    Datos procesados de los embalses de España.
    """

    return raw_embalses.select(
        pl.col("fecha"),
        pl.col("embalse_nombre").alias("embalse"),
        pl.col("ambito_nombre").alias("cuenca"),
        pl.col("agua_actual"),
        pl.col("agua_total"),
        pl.col("Porcentaje_Reserva").alias("porcentaje_agua"),
        pl.col("energia_actual"),
        pl.col("energia_total"),
        pl.col("Porcentaje_Energia").alias("porcentaje_energia"),
        pl.col("Uso").alias("uso"),
        pl.col("Variacion_Reserva").alias("variacion_agua"),
        pl.col("Variacion_Energia").alias("variacion_energia"),
        pl.col("Variacion_Porcentaje").alias("variacion_porcentaje_agua"),
        pl.col("Variacion_Porcentaje_Energia").alias("variacion_porcentaje_energia"),
        pl.col("Estado_Porc").alias("estado_agua"),
        pl.col("Estado_Porcentaje_Energia").alias("estado_energia"),
        pl.col("electrico_flag").alias("es_electrico"),
    )
