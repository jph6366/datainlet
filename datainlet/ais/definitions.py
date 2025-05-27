#!/usr/bin/env python3

import dagster as dg

from datainlet.ais import assets
from datainlet.resources import duckdb_resource, io_manager

definitions = dg.Definitions(
    assets=dg.load_assets_from_modules([assets]),
    resources={
        "io_manager": io_manager,
        "database": duckdb_resource
    }
)
