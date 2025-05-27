#!/usr/bin/env python3

import dagster as dg
from datainlet.aws import assets

definitions = dg.Definitions(
    assets=dg.load_assets_from_modules([assets]),
)
