import dagster as dg

import datalia.aemet.definitions as aemet_definitions
import datalia.dbt.definitions as dbt_definitions
import datalia.huggingface.definitions as huggingface_definitions
import datalia.ine.definitions as ine_definitions

definitions = dg.Definitions.merge(
    aemet_definitions.definitions,
    ine_definitions.definitions,
    dbt_definitions.definitions,
    huggingface_definitions.definitions,
)
