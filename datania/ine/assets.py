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
