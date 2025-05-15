import dagster as dg

import datainlet.gisd.definitions as gisd_definitions
import datainlet.sourcecoop.definitions as nwi_definitions
import datainlet.aws.definitions as ept_definitions
definitions = dg.Definitions.merge(
    gisd_definitions.definitions,
    nwi_definitions.definitions,
    ept_definitions.definitions

)
