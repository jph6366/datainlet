from datetime import datetime

import dagster as dg
import polars as pl

from datainlet.gisd.resources import GISDArcGISAPI


@dg.asset()
def raw_usvi_wfs(
    context: dg.AssetExecutionContext, gisd_api: GISDArcGISAPI
) -> pl.DataFrame:
    
    df = pl.DataFrame()

    response = gisd_api.get_us_virgin_islands()
    if response["features"]:
        mdf = pl.from_records(
            [elem["attributes"] for elem in response["features"]],
            infer_schema_length=None,
        )
        df = pl.concat([df, mdf], how="diagonal_relaxed")
        
    return df

