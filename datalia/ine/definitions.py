import dagster as dg

from datalia.ine import assets
from datalia.resources import io_manager

ine_assets = dg.load_assets_from_modules([assets])

definitions = dg.Definitions(
    assets=ine_assets,
    resources={"io_manager": io_manager},
)
