import dagster as dg

from datainlet.huggingface.assets import assets
from datainlet.huggingface.resources import HuggingFaceDatasetPublisher

definitions = dg.Definitions(
    assets=assets,
    resources={
        "dp": HuggingFaceDatasetPublisher(hf_token=dg.EnvVar("HUGGINGFACE_TOKEN"))
    },
)
