import dagster as dg

from datainlet.gisd import assets
from datainlet.gisd.resources import GISDArcGISAPI

definitions = dg.Definitions(
    assets=dg.load_assets_from_modules([assets]),
    resources={
        "gisd_api": GISDArcGISAPI(),
    },
)
