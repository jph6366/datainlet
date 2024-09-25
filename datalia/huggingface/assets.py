import polars as pl
from dagster import AssetIn, asset

from datalia.huggingface.resources import HuggingFaceDatasetPublisher


def create_hf_asset(dataset_name: str):
    @asset(name="huggingface_" + dataset_name, ins={"data": AssetIn(dataset_name)})
    def hf_asset(data: pl.DataFrame, dp: HuggingFaceDatasetPublisher) -> None:
        """
        Materialización del dataset en HuggingFace Datasets.
        """

        readme_content = f"""
---
license: mit
---
# {dataset_name}

Este conjunto de datos ha sido producido y publicado automáticamente por [Datalia](https://github.com/davidgasquez/datalia), una plataforma de datos abiertos moderna.

## Detalles del Conjunto de Datos

- **Número de filas:** {data.shape[0]}
- **Número de columnas:** {data.shape[1]}
        """

        dp.publish(
            dataset=data,
            dataset_name=dataset_name,
            username="datania",
            readme=readme_content,
            generate_datapackage=True,
        )

    return hf_asset


datasets = ["ipc"]

assets = []
for dataset in datasets:
    a = create_hf_asset(dataset)
    assets.append(a)
