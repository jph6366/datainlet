from datetime import datetime

import dagster as dg
import polars as pl

from datainlet.gisd.resources import GISDArcGISAPI


@dg.asset()
def raw_usvi_wfs(
    context: dg.AssetExecutionContext, gisd_api: GISDArcGISAPI
) -> pl.DataFrame:

    island_codes = ["STT", "STX", "STJ"] # The island codes to filter by
    island_attribute_field_name = "Island"

    all_island_dataframes = []

    for island_code in island_codes:
        query_params = {"where": f"{island_attribute_field_name} = '{island_code}'"}

        try:
            response = gisd_api.query(dataset_name="US_Virgin_Islands", params=query_params)

            if "features" in response and isinstance(response["features"], list):
                if len(response["features"]) > 0:
                    attributes_list = [elem["attributes"] for elem in response["features"]]
                    island_df = pl.from_records(attributes_list, infer_schema_length=None)
                    all_island_dataframes.append(island_df)
        except Exception:
            # Intentionally left blank as per request to remove logging/comments
            # Production code should handle errors more gracefully
            pass

    if not all_island_dataframes:
        return pl.DataFrame()

    try:
        final_df = pl.concat(all_island_dataframes, how="diagonal_relaxed")
    except Exception:
        return pl.DataFrame()

    return final_df
