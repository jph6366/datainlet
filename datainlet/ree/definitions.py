import dagster as dg

from datania.ree import assets
from datania.resources import io_manager

ree_assets = dg.load_assets_from_modules([assets])

definitions = dg.Definitions(
    assets=ree_assets,
    resources={"io_manager": io_manager},
)
