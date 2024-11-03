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
    Datos de la serie histórica de Hipotecas en España.

    Fuente: https://www.ine.es/dynt3/inebase/es/index.htm?padre=1043
    """
    BASE_URL = "https://www.ine.es/jaxiT3/files/t/es/csv_bdsc/"

    resultados_urls = [
        {
            "id": 3200,
            "name": "Hipotecas constituidas sobre el total de fincas por naturaleza de la finca",
        },
        {
            "id": 3202,
            "name": "Hipotecas constituidas sobre el total de fincas por entidad que concede el préstamo",
        },
        {
            "id": 3203,
            "name": "Hipotecas constituidas sobre fincas rústicas por entidad que concede el préstamo",
        },
        {
            "id": 3204,
            "name": "Hipotecas constituidas sobre fincas urbanas por entidad que concede el préstamo",
        },
        {
            "id": 3205,
            "name": "Hipotecas con cambios registrales sobre el total de fincas por naturaleza de la finca",
        },
        {
            "id": 3206,
            "name": "Hipotecas con cambios registrales sobre el total de fincas por tipo de cambio",
        },
        {
            "id": 3209,
            "name": "Hipotecas canceladas registralmente sobre el total de fincas por naturaleza de la finca y entidad prestamista",
        },
    ]

    dfs = [
        pl.read_csv(
            BASE_URL + f"{resultado['id']}.csv",
            truncate_ragged_lines=True,
            separator=";",
            infer_schema_length=None,
        )
        for resultado in resultados_urls
    ]

    dfs = [
        df.with_columns(pl.lit(resultado["name"]).alias("Tabla"))
        for df, resultado in zip(dfs, resultados_urls)
    ]

    # Get a list of columns from each dataframe
    column_sets = [set(df.columns) for df in dfs]

    # Find the intersection of all column sets
    common_columns = set.intersection(*column_sets)

    processed_dfs = [
        df.with_columns(
            pl.concat_str(
                [pl.col(i) for i in df.columns if i not in common_columns],
                separator=" - ",
            ).alias("Variable"),
            pl.col("Total").cast(pl.String),
        ).drop(list(set(df.columns) - common_columns))
        for df in dfs
    ]
    # Concatenate all processed dataframes vertically
    combined_df = pl.concat(processed_dfs)

    combined_df = combined_df.with_columns(
        pl.concat_str([pl.col("Tabla"), pl.col("Variable")], separator=" - ").alias(
            "Tabla y Variable"
        )
    ).drop(["Tabla", "Variable"])

    combined_df = combined_df.with_columns(
        pl.col("Total").str.replace_all(r"\.", "").cast(pl.Int64)
    )

    # Convert Periodo from format like "2024M08" to proper dates
    combined_df = combined_df.with_columns(
        pl.col("Periodo")
        .str.replace("M", "-")
        .alias("Periodo")
        .str.strptime(pl.Date, "%Y-%m")
    )

    # If we want to pivot the dataframe to have a column for each variable (wide format)
    # df = combined_df.pivot(
    #     on="Tabla y Variable",
    #     index=["Provincias", "Periodo"],
    #     values="Total"
    # )

    return combined_df
