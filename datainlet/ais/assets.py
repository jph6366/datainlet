#!/usr/bin/env python3

#
# Fast Top N Aggregation and Filtering with DuckDB
# in a geospatial context
# How to find the maximum draft of spatial bins,
# grouping by the spatial index and extracting
# the maximum draft value using a nested structure
import os
import threading
import concurrent.futures as cf
import dagster as dg
from dagster_duckdb import DuckDBResource

import tqdm
import httpx
import polars as pl
from pyarrow import csv, table

def connect_to_duckdb(database: DuckDBResource,
                      progress_bar=False,
                      db_threads=os.cpu_count(),
                      memory_limit=None,
                      tmp_dir=None,
                      tmp_size=None):

    conn = database.get_connection()
    conn.sql("INSTALL")
    conn.sql("LOAD SPATIAL")
    conn.sql("INSTALL H3 FROM community")
    conn.sql("LOAD H3")

    conn.sql(f"SET enable_progress_bar={progress_bar}")
    conn.sql(f"SET threads={db_threads}")

    if memory_limit is not None:
        conn.sql(f"SET memory_limit='{memory_limit}'")
    if tmp_dir is not None:
        conn.sql(f"SET temp_directory='{tmp_dir}'")
    if tmp_size is not None:
        conn.sql(f"SET max_temp_directory_size='{tmp_size}'")

    return conn

def get_dtypes():

    pd_dtypes={
        'MMSI': 'string',
        'BASEDATETIME': 'string',
        'LAT': 'float64',
        'LON': 'float64',
        'SOG': 'float32',
        'COG': 'float32',
        'HEADING': 'float32',
        'VESSELNAME': 'string',
        'IMO': 'string',
        'CALLSIGN': 'string',
        'VESSELTTYPE': 'float32',
        'STATUS': 'float32',
        'LENGTH': 'float32',
        'WIDTH': 'float32',
        'DRAFT': 'float32',
        'CARGO': 'string',
        'TRANSCEIVERCLASS': 'string'
    }

    return pd_dtypes


def mk_points(conn, use_primary_key=False, append=False):

    if not append:
        conn.sql("DROP TABLE IF EXISTS ais_points")

    if use_primary_key:
        p_key = ", PRIMARY KEY (H3_15)"
    else:
        p_key = ""

    conn.sql(f"""
    CREATE TABLE IF NOT EXISTS ais_points (
        H3_15 UBIGINT,
        MMSI VARCHAR,
        BASEDATETIME TIMESTAMP,
        LAT DOUBLE,
        LON DOUBLE,
        SOG FLOAT,
        COG FLOAT,
        HEADING FLOAT,
        VESSELNAME VARCHAR,
        IMO VARCHAR,
        CALLSIGN VARCHAR,
        VESSELTYPE SMALLINT,
        STATUS SMALLINT,
        LENGTH FLOAT,
        WIDTH FLOAT,
        DRAFT FLOAT,
        CARGO VARCHAR,
        TRANSCEIVERCLASS VARCHAR,
        WKB GEOMETRY {p_key}
    )
"""
             )


def mk_bins(conn, use_primary_key=False, append=False):
    if not append:
        conn.sql("DROP TABLE IF EXISTS ais_bins")

    p_key = ", PRIMARY KEY (H3_4, H3_11)" if use_primary_key else ""

    conn.sql(f"""
        CREATE TABLE ais_bins (
            H3_4 UBIGINT,
            H3_11 UBIGINT,
            DRAFT FLOAT {p_key}
    )
    """
    )


def df_chunk_to_duckdb(conn, chunk, h3_level=15):

    conn.register('ais_df', chunk)
    conn.sql("BEGIN TRANSACTION")
    conn.sql(f"""
        WITH temp_ais_points as (
            SELECT
                h3_latlng_to_cell(LAT, LON, {h3_level}) AS H3_{h3_level},
                unnest(
                     max_by(COLUMNS(*), DRAFT, 1),
                     recursive := 1
                ),
                ST_POINT(
                     h3_cell_to_lng(
                         h3_latlng_to_cell(LAT, LON, {h3_level})
                     ),
                     h3_cell_to_lat(
                         h3_latlng_to_cell(LAT, LON, {h3_level})
                     )
                ) as WKB
            FROM ais_df
            GROUP BY H3_{h3_level}
            GROUP BY H3_{h3_level}
       )
       INSERT INTO ais_points
       SELECT * FROM temp_ais_points
       ON CONFLICT (H3_{h3_level}) DO UPDATE SET
           MMSI = excluded.MMSI,
           BASEDATETIME = excluded.BASEDATETIME,
           LAT = excluded.LAT,
           LON = excluded.LON,
           SOG = excluded.SOG,
           COG = excluded.COG,
           HEADING = excluded.HEADING,
           VESSELNAME = excluded.VESSELNAME,
           IMO = excluded.IMO,
           CALLSIGN = excluded.CALLSIGN
           VESSELTYPE = excluded.VESSELTYPE
           STATUS = excluded.STATUS,
           LENGTH = excluded.LENGTH,
           WIDTH = excluded.WIDTH,
           DRAFT = excluded.DRAFT,
           CARGO = excluded.CARGO,
           TRANSCEIVERCLASS = excluded.TRANSCEIVERCLASS,
           WKB = excluded.WKB
       WHERE
           ais_points.DRAFT < excluded.DRAFT
    """)
    conn.sql("COMMIT")
    conn.unregister("ais_df")



def ais_to_duckdb(
        db_file,
        lock,
        year,
        month,
        day,
        db_threads=os.cpu_count()
):

    ais_url = f"https://coast.noaa.gov/htdata/CMSP/AISDataHandler/{year}"
    ais_file = f"{ais_url}/AIS_{year}_{month}_{day}.zip"

    ais_raw = httpx.get(
        ais_file
        ,verify=False
    )

    with open(f"data/raw/AIS_{year}_{month}_{day}", "wb") as output_file:
        output_file.write(ais_raw.content)

    conn = connect_to_duckdb(db_file, db_threads=db_threads)
    pd_dtypes = get_dtypes()
    chunk_size = 10000
    with csv.read_csv(
        f"data/raw/AIS_{year}_{month}_{day}",
        read_options=csv.ReadOptions(
            skip_rows=1,
            column_names=list(pd_dtypes.keys()),
            block_size=chunk_size
        ),
        convert_options=csv.ConvertOptions(column_types=pd_dtypes)
    ) as reader:
        for chunk in reader:
            with lock:
                df_chunk_to_duckdb(conn, chunk)

    conn.close()
    return ais_file


def ais_to_parquet(
        src_dir,
        year, month, day,
        overwrite=False,
        db_file=None,
        db_threads=os.cpu_count()
):
    ais_url = f"https://coast.noaa.gov/htdata/CMSP/AISDataHandler/{year:04d}"
    ais_file = f"{ais_url}/AIS_{year:04d}_{month:02d}_{day:02d}.zip"

    ais_raw = httpx.get(
        ais_file
    )

    with open(f"data/raw/AIS_{year:04d}_{month:02d}_{day:02d}", "wb") as output_file:
        output_file.write(ais_raw.content)

    parquet_file = f"data/raw/AIS_{year:04d}.parquet"
    conn = connect_to_duckdb(db_file=db_file, db_threads=db_threads)
    pd_dtypes = get_dtypes()
    df = pl.read_csv(
        f"data/raw/AIS_{year:04d}_{month:02d}_{day:02d}",
        skip_rows=1,
        Header=False,
        new_columns=list(pd_dtypes.keys()),
        schema_overrides=pd_dtypes
    )

    df.unique(subset=['MMSI','BASEDATETIME'])

    conn.register('ais_df', df)
    conn.sql(f"""
        COPY (
            FROM ais_df
            SELECT
                h3_latlng_to_cell(LAT, LON, 15) AS H3_15,
                unnest(
                    max_by(COLUMNS(*), DRAFT, 1),
                    recursive := 1
                ),
                ST_POINT(
                    h3_cell_to_lng(
                        h3_latlng_to_cell(LAT, LON, 15)
                    ),
                    h3_cell_to_lat(
                        h3_latlng_to_cell(LAT, LON, 15)
                    )
                ) AS WKB
            GROUP BY H3_15
            ORDER BY H3_15
        ) TO '{parquet_file}' (FORMAT PARQUET)
    """
    )

    conn.unregister("ais_df")
    del df

    conn.close()
    return parquet_file

######################
## Secondary query to rebin AIS data into additional bins
##
##   If we want to rebin or take those 1 meter bins
##   then group them into a lower resolution spatial bin
##   for aggregation or for efficient geoparquet.
##
##  we can take our time window invariants
##  we can rebin the daily files into larger time aggregate files
##  we can also change the spatial partitioning for each of those time windows
##
## conn.sql(f"""
##     COPY(
##         FROM '{parquet_in}'
##         SELECT h3_cell_to_parent(h3_15, 11) AS H3_11,
##             unnest(
##                 max_by(COLUMNS(*), DRAFT, 1),
##                 recursive := 1
##             ),
##             h3_cell_to_lat(H3_11) AS LAT,
##             h3_cell_to_lng(H3_11) AS LON,
##             ST_POINT(h3_cell_to_lng(H3_11), h3_cell_to_lat(H3_11)) AS WKB
##         GROUP BY H3_11
##         ORDER BY H3_11
##     ) TO '{parquet_out}' (FORMAT PARQUET)
## """
##)
##
##
##
##
##
##
##
##
##

@dg.asset()
def noaa_ais_duckdb(database: DuckDBResource):
    ais_dir = os.path.join("data/raw/", 'downloads')
    os.makedirs(ais_dir, exist_ok=True)
    lock = threading.Lock()
    ais_to_duckdb(
        database,
        lock,
        year='2024',
        month='01',
        day='01'
    )



@dg.asset()
def noaa_ais_geoparquet(database: DuckDBResource):
    ais_dir = os.path.join("data/raw/", 'downloads')
    os.makedirs(ais_dir, exist_ok=True)

    ncores = os.cpu_count()
    duck_threads = 7
    python_threads = 2

    lock = threading.Lock()
    with cf.ProcessPoolExecutor(max_workers=python_threads) as executor:
        futures = [
            executor.submit(ais_to_parquet,
                            src_dir=ais_dir,
                            year='2024',
                            month='01',
                            day='01',
                            db_file=database,
                            db_threads=duck_threads,
                            overwrite=False
                    )
        ]
        with tqdm(tota=len(futures), unit="file") as prog_bar:
            for future in cf.as_completed(futures):
                try:
                    result = future.result().replace(f"{ais_dir}{os.path.sep}", '')
                except:
                    result = "No Data"
                prog_bar.set_description(f"{result}")
                prog_bar.update(1)



## def noaa_ais_stac_geoparquet():
