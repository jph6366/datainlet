import dagster as dg

import datania.aemet.definitions as aemet_definitions
import datania.dbt.definitions as dbt_definitions
import datania.huggingface.definitions as huggingface_definitions
import datania.ine.definitions as ine_definitions

definitions = dg.Definitions.merge(
    aemet_definitions.definitions,
    ine_definitions.definitions,
    dbt_definitions.definitions,
    huggingface_definitions.definitions,
)
