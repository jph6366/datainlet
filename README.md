<!-- markdownlint-disable MD033 MD041-->

<p align="center">
  <h1 style="font-size:80px; font-weight: 800;" align="center">D A T A I S L E</h1>
  
   <h4 style="font-size:80px; font-weight: 800;" align="center">Making Better Land and Water Use Decisions, Protecting Natural Resources, and Planning for a Sustainable Future</h4>
  
</p>


<div align="center">
  <img alt="GitHub" src="https://img.shields.io/github/license/davidgasquez/datania?style=flat-square">
  <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/davidgasquez/datania/ci.yml?style=flat-square">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/davidgasquez/datania?style=flat-square">
</div>

<br>

Dataisle is a priority-resilience, asset-centric open data platform that encourages heterogeneous chunks of resources and jobs to capture some understanding of land and water use for the USVI.

## 💡 Principles

- **Transparency** : Code, standards, infrastructure, and data are public. Use open tools, standards, and infrastructure, and share data in accessible formats .
- **Modularity** : Each component or dataset can be replaced, extended, or removed. The code works well in many environments (a laptop, a cluster, or from the browser) and can be deployed in different locations.
- **Frictionless** : Don't ask, fork and improve your code, models, or add a new data source. Use datasets without API limits or quotas.
-**Data as Code** : Declarative transformations tracked in git. Datasets and their transformations are published so others can build on them.
- **Glue** : Datania is a bridge between tools and approaches, not a standard or a tool in itself. It integrates with other tools and services.
- **Reslience**: The islands of St. Croix, St. Thomas, and St. John are small; the ridge-to-reef watershed connection is a visible part of lived experience and critical to effective coastal zone management.
    - According to NOAA, the entire USVI territory - and all its watersheds - is considered to
    be the coastal zone. However, the USVI has historic and chronic deficiencies in watershed-scale land
    and water use planning as well as data availability. The small watersheds, steep slopes, and lack of
    comprehensive planning in development all contribute to growing problems related to stormwater,
    flooding, erosion, pollution, coastal runoff, groundwater, and drought. These problems are intensified
    by climate change and social vulnerability. Local agency staff and community members often lack
    robust environmental literacy (defined as “positive affect, understanding, skills, and environmentally
    responsible behaviors”) regarding coastal processes, steep slopes, and geospatial data, which can
    hinder the necessary buy-in from resource managers and the community regarding resilience projects

## ⚙️ Configuración

Si quieres contribuir, es fácil! Clona el repositorio y sigue estas instrucciones.

Cualquier problema que encuentres, no dudes en [abrir una issue](https:github.com/davidgasqyez/datania/issues/new)!

### 🐍 Python

Instala Python en tu sistema y opcionalmente, [`uv`](https://github.com/astral-sh/uv).

Si tienes `uv`, puedes instalar todas las dependencias dentro de un entorno virtual de Python ejecutando `make setup` una vez hayas clonado el repositorio.

```bash
make setup
```

Si no quieres instalar `uv`, puedes usar Python para crear un entorno virtual y instalar las dependencias.

```bash
python3 -m venv .venv
source .venv/bin/activate

# Install the package and dependencies
pip install -e ".[dev]"
```

Ahora, puedes ejecutar `make dev` para iniciar el servidor de Dagster.

### 🌍 Variables de Entorno

Para poder acceder a las fuentes de datos y publicar datasets, hace falta definir las siguientes variables de entorno:

- `AEMET_API_TOKEN`: Token para acceder a la API de AEMET.
- `HUGGINGFACE_TOKEN`: Token para publicar datasets en HuggingFace.
- `DATABASE_PATH`: Ruta al archivo de la base de datos DuckDB (por defecto es `./data/database.duckdb`).

Puedes definir estas variables en un archivo `.env` en la raíz del proyecto o configurarlas en tu entorno de desarrollo.

## 📦 Estructura

Datania está compuesta por varios componentes:

- **Dagster**: Una herramienta que orquesta los pipelines de datos.
- **DuckDB y Polars**: Base de datos y librería de procesamiento de datos.
- **HuggingFace**: Plataforma donde publicamos los datasets.

## 📄 Licencia

Datania es un proyecto de código abierto bajo la licencia [MIT](LICENSE).
