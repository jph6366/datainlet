<!-- markdownlint-disable MD033 MD041-->

<p align="center">
  <h1 style="font-size:80px; font-weight: 800;" align="center">D A T A  I N L E T</h1>
</p>

<div align="center">
  <img alt="GitHub" src="https://img.shields.io/github/license/davidgasquez/datania?style=flat-square">
  <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/davidgasquez/datania/ci.yml?style=flat-square">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/davidgasquez/datania?style=flat-square">
</div>

<br>
 <h4 style="font-size:80px; font-weight: 800;" align="center">datainlet is a priority-resilience, asset-centric open data platform that joins heterogeneous chunks of resources, jobs, and metadata to capture some understanding of land and water use for the USVI.</h4>

## 🌞 Principles

- **Transparency** : Code, standards, infrastructure, and data are public. Use open tools, standards, and infrastructure, and share data in accessible formats .

- **Modular and Interoperable** : Each component can be replaced, extended, or removed. Works well in many environments (your laptop, in a cluster, or from the browser), can be deployed to many places  and integrates with multiple tools. Use open tools, standards, infrastructure, and share data in accessible formats.

- **Frictionless** : Don't ask, fork and improve your code, models, or add a new data source. Use datasets without API limits or quotas.

- **Data as Code** : Declarative transformations tracked in git. Datasets and their transformations are published so others can build on them.

- **Stateless and serverless**: as much as possible. E.g. use GitHub Pages, host datasets on S3, interface with HTML, JavaScript, and WASM. No servers to maintain, no databases to manage, no infrastructure to worry about. Keep infrastructure management lean.

- **Glue** : GDAL/OGR and PDAL are tools that support tons of geospatial raster and vector formats, and pointcloud formats. datainlet is a bridge between tools and approaches, so we want to ensure that your data platform isn't GDAL in a Dagster trench coat. Instead we enable modular design of ingesting and staging of data that is idiomatic and asset-centric from start to end

- **[#beFAIRandCARE](https://opencontext.org/about/fair-care)** :
     <h3 style="font-size:80px; font-weight: 800;" align="center"> Findability, Accessibility, Interoperability, Reuse of digital assets,</h3>
          <h3 style="font-size:80px; font-weight: 800;" align="center"> and</h3>
     <h3 style="font-size:80px; font-weight: 800;" align="center"> Collective Benefit, Authority To Control, Responsibility, Ethics </h3>

- **[IOCM](https://iocm.noaa.gov/)** : Integrated Ocean and Coastal Mapping is the practice of planning, acquiring, integrating, and sharing ocean and coastal data and related products so that people who need the data can find it and use it easily:
     <h3 style="font-size:80px; font-weight: 800;" align="center">Map Once, Use Many Times.</h3>

- **No vendor lock-in** :

<h4 style="font-size:80px; font-weight: 800;" align="center">
  Rely on Open code, standards, and infrastructure.

  Use the tool you want to create, explore, and consume the datasets.

  Agnostic of any tooling or infrastructure provider.

  Standard format for data and APIs!

  Keep your data as future-friendly and future-proof as possible!
</h4>

- **Coastal and Climate Resilience**: To be successful, these diverse projects require buy-in from many levels of the community: decision makers, local agency staff, homeowners, real estate professionals, and design, construction, and maintenance contractors.

    _From Planning to Action for Coastal Resilience:_

    _Elevating Environmental Literacy for USVI Priority Resilience Projects_

## ⚙️ Configuration

If you want to contribute, it's easy! Clone the repository and follow these instructions.

Any problems you encounter, please feel free to open an issue !

### 🐍 Python

Install Python on your system and optionally, uv.

If you have uv, you can install all dependencies inside a Python virtual environment by running make setup once you have cloned the repository.

```bash
make setup
```

If you don't want to install uv, you can use Python to create a virtual environment and install dependencies.

``` bash
python3 -m venv .venv
source .venv/bin/activate

# Install the package and dependencies
pip install -e ".[dev]"
```

Now, you can run make dev to start the Dagster server.

### 🌍 Environment Variables

To access data sources and publish datasets, the following environment variables must be defined:

- AEMET_API_TOKEN: Token to access the AEMET API.
- HUGGINGFACE_TOKEN: Token to publish datasets on HuggingFace.
- DATABASE_PATH: Path to the DuckDB database file (default is ./data/database.duckdb).

You can define these variables in a file .env at the root of your project or configure them in your development environment.

## 📦 Structure

datainlet is composed of several components:

- Dagster : A tool that orchestrates data pipelines.
- DuckDB and Polars : Database and data processing library.
- HuggingFace : Platform where we publish the datasets.

## 📄 License

datainlet is an open source project under the MIT license.
