import dagster as dg

from datania.dbt import assets
from datania.dbt.resources import dbt_resource

aemet_assets = dg.load_assets_from_modules([assets])

definitions = dg.Definitions(assets=aemet_assets, resources={"dbt": dbt_resource})
