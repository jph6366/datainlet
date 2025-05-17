#!/usr/bin/env python3

import dagster as dg
from dagstermill import ConfigurableLocalOutputNotebookIOManager
from datainlet.aws import assets

definitions = dg.Definitions(
    assets=dg.load_assets_from_modules([assets]),
    resources={
        "output_notebook_io_manager": ConfigurableLocalOutputNotebookIOManager()
    }
)
