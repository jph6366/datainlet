import dagster as dg
import polars as pl


@dg.asset(
    retry_policy=dg.RetryPolicy(max_retries=5),
)
def raw_ipc() -> pl.DataFrame:
    """
    Datos de la serie histórica del Índice de Precios de Consumo (IPC) en España en formato CSV.
    """

    df = pl.read_csv(
        "https://www.ine.es/jaxiT3/files/t/csv_bdsc/50904.csv", separator=";"
    )

    return df


@dg.asset()
def raw_hipotecas() -> pl.DataFrame:
    """
    Datos de la serie histórica de hipotecas constituidas en España en formato CSV.

    Fuente: https://www.ine.es/dynt3/inebase/es/index.htm?padre=1043
    """
    url = "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/3200.csv?nocab=1"
    df = pl.read_csv(
        url, truncate_ragged_lines=True, separator=";", infer_schema_length=None
    )

    df = df.with_columns(
        [
            pl.col("Periodo")
            .str.strptime(pl.Date, format="%YM%m", strict=False)
            .alias("Periodo"),
            pl.col("Total").str.replace_all("[^0-9]", "").cast(pl.Int64),
        ]
    )

    df = df.pivot(on="Número e importe", values="Total")

    df = df.rename(
        {
            col: col.lower()
            .replace(" ", "_")
            .replace("ú", "u")
            .replace("é", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("á", "a")
            .replace("ñ", "n")
            for col in df.columns
        }
    )

    return df
