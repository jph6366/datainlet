#!/usr/bin/env python3

import dagster as dg

from datainlet.ais import assets
from datainlet.resources import duckdb_resource

definitions = dg.Definitions(
    assets=dg.load_assets_from_modules([assets]),
    resources={
        "database": duckdb_resource
    }

)
