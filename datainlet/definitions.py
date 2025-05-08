import dagster as dg

import datainlet.gisd.definitions as gisd_definitions

definitions = dg.Definitions.merge(
    gisd_definitions.definitions
)
