import dagster as dg

from datania.huggingface.assets import assets
from datania.huggingface.resources import HuggingFaceDatasetPublisher

definitions = dg.Definitions(
    assets=assets,
    resources={
        "dp": HuggingFaceDatasetPublisher(hf_token=dg.EnvVar("HUGGINGFACE_TOKEN"))
    },
)
