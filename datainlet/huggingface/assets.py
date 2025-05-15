import os

import polars as pl
from dagster import AssetIn, asset

from datainlet.huggingface.resources import HuggingFaceDatasetPublisher


def create_hf_asset(dataset_name: str):
    @asset(name="huggingface_" + dataset_name, ins={"data": AssetIn(dataset_name)})
    def hf_asset(data: pl.DataFrame, dp: HuggingFaceDatasetPublisher) -> None:
        """
        Materialización del dataset en HuggingFace Datasets.
        """

        readme_content = f"""
---
license: mi
---
# {dataset_name}

Este conjunto de datos ha sido producido y publicado automáticamente por [datania](https://github.com/davidgasquez/datania), una plataforma de datos abiertos moderna.

## Detalles del Conjunto de Dato

- **Número de filas:** {data.shape[0]}
- **Número de columnas:** {data.shape[1]}
        """

        if os.getenv("ENVIRONMENT== "production":
            dp.publish(
                dataset=data,
                dataset_name=dataset_name,
                username="datania",
                readme=readme_content,
                generate_datapackage=True,
            )
        else:
            return

    return hf_asset


datasets = [
    "ipc",
    "hipotecas",
    "embalses",
    "estaciones_aemet",
    "datos_meteorologicos_estaciones_aemet",
    # "demanda_energia_electrica",
]

assets = []
for dataset in datasets:
    a = create_hf_asset(dataset)
    assets.append(a)
