import dagster as dg

from datania.ine import assets
from datania.resources import io_manager

ine_assets = dg.load_assets_from_modules([assets])

definitions = dg.Definitions(
    assets=ine_assets,
    resources={"io_manager": io_manager},
)
