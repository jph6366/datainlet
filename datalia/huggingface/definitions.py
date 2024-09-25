import dagster as dg

from datalia.huggingface.assets import assets
from datalia.huggingface.resources import HuggingFaceDatasetPublisher

definitions = dg.Definitions(
    assets=assets,
    resources={
        "dp": HuggingFaceDatasetPublisher(hf_token=dg.EnvVar("HUGGINGFACE_TOKEN"))
    },
)
