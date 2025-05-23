import dagster as dg

import datainlet.gisd.definitions as gisd_definitions
import datainlet.sourcecoop.definitions as nwi_definitions
import datainlet.ais.definitions as ais_definitions

definitions = dg.Definitions.merge(
    gisd_definitions.definitions,
    nwi_definitions.definitions,
    ais_definitions.definitions
)
