from dagster import Definitions
from .assets import energy_demand_data

from datania.resources import io_manager

definitions = Definitions(
    assets=[energy_demand_data],
    resources={"io_manager": io_manager},
)
