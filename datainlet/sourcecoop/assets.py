#!/usr/bin/env python3
import asyncio
import dagster as dg
from dagster_duckdb import DuckDBResource
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
import polars as pl

@dg.asset(
    group_name="raw_nwi"
)
def GISWQS_NWI_parquet() -> dg.MaterializeResult:

    endpoint: str = (
        "https://data.source.coop/giswqs/nwi/wetlands"
    )

    file_url = f"{endpoint}/NC_Wetlands.parquet"

    raw_nwi = httpx.get(
        file_url
    )

    with open("data/raw/NC_Wetlands.parquet", "wb") as output_file:
        output_file.write(raw_nwi.content)

    num_rows = len(pl.read_parquet("data/raw/NC_Wetlands.parquet"))

    return dg.MaterializeResult(
        metadata={
            'Number of records': dg.MetadataValue.int(num_rows)
        }
    )


@dg.asset(
    deps=["GISWQS_NWI_parquet"],
    group_name="ingested",
)
def GISWQS_NWI(database: DuckDBResource) -> None:


    query = f"""
    -- Drop the table if it exists to start fresh for this example run,
    -- or use CREATE TABLE IF NOT EXISTS for idempotent operations.
    -- DROP TABLE IF EXISTS wetlands_data;

    CREATE TABLE IF NOT EXISTS wetlands_data (
        attribute VARCHAR,
        wetland_type VARCHAR,
        acres DOUBLE,
        shape_length DOUBLE,
        shape_area DOUBLE,
        geometry BLOB
       );

    DELETE FROM wetlands_data;

    INSERT INTO wetlands_data (
        attribute,
        wetland_type,
        acres,
        shape_length,
        shape_area,
        geometry
    )
    SELECT
        ATTRIBUTE,       -- Column names from your Parquet file
        WETLAND_TYPE,
        ACRES,
        Shape_Length,    -- Note: Parquet column names can be case-sensitive
        Shape_Area,      -- Ensure these match exactly what's in the Parquet file
        geometry
    FROM read_parquet("data/raw/NC_Wetlands.parquet");
    """

    with database.get_connection() as conn:
        conn.execute(query)
