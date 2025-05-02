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
 <h4 style="font-size:80px; font-weight: 800;" align="center">Dataisle is a priority-resilience, asset-centric open data platform that encourages heterogeneous chunks of resources, jobs, and metadata to capture some understanding of land and water use for the USVI.</h4>

## 🌞 Principles

- **Transparency** : Code, standards, infrastructure, and data are public. Use open tools, standards, and infrastructure, and share data in accessible formats .

- **Modularity** : Each component or dataset can be replaced, extended, or removed. The code works well in many environments (a laptop, a cluster, or from the browser) and can be deployed in different locations.

- **Frictionless** : Don't ask, fork and improve your code, models, or add a new data source. Use datasets without API limits or quotas.

- **Data as Code** : Declarative transformations tracked in git. Datasets and their transformations are published so others can build on them.

- **Glue** : Datania is a bridge between tools and approaches, not a standard or a tool in itself. It integrates with other tools and services.

- **[FAIR](https://www.go-fair.org/fair-principles/)**

- **Coastal and Climate Resilience**: To be successful, these diverse projects require buy-in from many levels of the community: decision makers, local agency staff, homeowners, real estate professionals, and design, construction, and maintenance contractors.

    _From Planning to Action for Coastal Resilience:_
    
    _Elevating Environmental Literacy for USVI Priority Resilience Projects_
    ```
    Improving the environmental literacy of these audiences on the specific topics of coastal processes,
    steep slopes, and geospatial data will increase their buy-in for the Territory’s Priority Resilience
    Projects listed below. Major partners in these projects include the Department of Public Works (DPW),
    the VI Territorial Emergency Management Authority (VITEMA), the Office of Disaster Recovery
    (ODR), the Department of Agriculture (DOA), and the University of the Virgin Islands (UVI).
    ```

## ⚙️ Configuración

If you want to contribute, it's easy! Clone the repository and follow these instructions.

Any problems you encounter, please feel free to open an issue !

### 🐍 Python

Install Python on your system and optionally, uv.

If you have uv, you can install all dependencies inside a Python virtual environment by running make setuponce you have cloned the repository.

```bash
make setup
```

If you don't want to install uv, you can use Python to create a virtual environment and install dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate

# Install the package and dependencies
pip install -e ".[dev]"
```

Now, you can run make devto start the Dagster server.

### 🌍 Variables de Entorno

To access data sources and publish datasets, the following environment variables must be defined:

- AEMET_API_TOKEN: Token to access the AEMET API.
- HUGGINGFACE_TOKEN: Token to publish datasets on HuggingFace.
- DATABASE_PATH: Path to the DuckDB database file (default is ./data/database.duckdb).

You can define these variables in a file .envat the root of your project or configure them in your development environment.

## 📦 Estructura

Datania is composed of several components:

- Dagster : A tool that orchestrates data pipelines.
- DuckDB and Polars : Database and data processing library.
- HuggingFace : Platform where we publish the datasets.

## 📄 Licencia

Datania es un proyecto de código abierto bajo la licencia [MIT](LICENSE).
