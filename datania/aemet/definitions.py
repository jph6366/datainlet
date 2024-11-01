import dagster as dg

from datania.aemet import assets
from datania.aemet.resources import AEMETAPI
from datania.resources import duckdb_resource

aemet_assets = dg.load_assets_from_modules([assets])

definitions = dg.Definitions(
    assets=aemet_assets,
    resources={
        "duckdb": duckdb_resource,
        "aemet_api": AEMETAPI(token=dg.EnvVar("AEMET_API_TOKEN")),
    },
)
