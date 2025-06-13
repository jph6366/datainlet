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
 <h4 style="font-size:80px; font-weight: 800;" align="center">datainlet is a coastal community-based, asset-centric open data platform. ⚠ work in progress ⚠ </h4>

 <p style="font-size:80px; font-weight: 800;" align="center"> Unifies and modernizes schools of data extracted from software-defined assets, resources, schedules, and sensors deployed in a Dagster project. </p>

## ⚙️ Configuration

If you want to contribute, it's easy! Clone the repository and follow these instructions.

Any problems you encounter, please feel free to open an issue !

### 🐍 Python

Install Python on your system and pixi.

If you have pixi, you can install all dependencies inside a Pixi virtual environment by running a pixi task once you have cloned the repository.

```bash
pixi run dev
```

### 🌍 Environment Variables

To access data sources and publish datasets, the following environment variables must be defined:

- AEMET_API_TOKEN: Token to access the AEMET API.
- HUGGINGFACE_TOKEN: Token to publish datasets on HuggingFace.
- DATABASE_PATH: Path to the DuckDB database file (default is ./data/database.duckdb).

You can define these variables in a file .env at the root of your project or configure them in your development environment.

## 📦 Structure

datainlet is composed of several components:

- Dagster and dbt : A tool that orchestrates data pipelines, and a transformation workflow that compiles and runs your analytics code against your data platform, enabling you and your team to collaborate on a single source of truth for metrics, insights, and business definitions.
- DuckDB and Pandas Polars : Database and DataFrames.
- GDAL and DuckDB Spatial Extension : Geo data abstraction library and a prototype of a geospatial extension for DuckDB.
- PDAL and TileDB : Point data abstraction library and Database.
- GeoParquet, GeoArrow :  geospatial data in Apache Arrow and Apache Parquet.
- STAC : common language to describe geospatial information, so it can more easily be worked with, indexed, and discovered.
- HuggingFace : Platform where we publish the datasets.

## 🌞 Principles

- **Transparency** : Code, standards, infrastructure, and data are public. Use open tools, standards, and infrastructure, and share data in accessible formats .

- **Modular and Interoperable** : Each component can be replaced, extended, or removed. Works well in many environments (your laptop, in a cluster, or from the browser), can be deployed to many places  and integrates with multiple tools. Use open tools, standards, infrastructure, and share data in accessible formats.

- **Frictionless** : Don't ask, fork and improve your code, models, or add a new data source. Use datasets without API limits or quotas.

- **Data as Code** : Declarative transformations tracked in git and data quality and insights embedded into Dagster. Datasets and their transformations are published so others can build on them. 

- **Stateless and serverless**: as much as possible. E.g. use GitHub Pages, host datasets on S3, interface with HTML, JavaScript, and WASM. No servers to maintain, no databases to manage, no infrastructure to worry about. Keep infrastructure management lean.

- **Glue** : datainlet is a bridge between tools and approaches, so we want to ensure that your data platform isn't just GDAL in a trench coat.
  - We enable modular asset materialization of ingesting and staging of raw and processed data that is transparent and asset-centric for the community configuration from start to completion.
    - DuckDB for a simple, portable, feature-rich, fast, Dagster-integrated RDBMS to provide high performance on complex queries against large databases in embedded configuration, such as combining tables with hundreds of columns and billions of rows.
    - TileDB for a single, unified solution that manages the geospatial data objects along with the raw original data (e.g., images, text files, etc), the ML embedding models, and all the other data modalities in your application

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

- **Resilience**: For communities to be successful, multi-stakeholder projects require buy-in from many levels of the community: decision makers, local agency staff, homeowners, real estate professionals, and design, construction, and maintenance contractors.
  - After pipelining your assets, resources, jobs, etc.; You should be able to immediately view your data tables and visualize complex insights using simple workflows ranging from databases, ArcGIS, QGIS, Jupyter Notebooks, MapLibre, and more to come.
  - Finally once all the inputs and ouputs are accounted for, accessible AI engineering assets should bolster the community of interest through environmental literacy and perhaps training in accessible AI engineering tools and workloads.


## Proof of Concept - Showcase Project
<h4 style="font-size:80px; font-weight: 800;" align="center">

  _From Planning to Action for Coastal Resilience:_

  _Elevating Environmental Literacy for USVI Priority Resilience Projects_

  https://huggingface.co/datasets/Jphardee/PRVI_Wetlands
</h4>



## 📄 License

datainlet is an open source project under the MIT license.
