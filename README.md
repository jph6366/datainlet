<!-- markdownlint-disable MD033 MD041-->

<p align="center">
  <h1 style="font-size:80px; font-weight: 800;" align="center">D A T A L I A</h1>
  <p align="center">Datos, sin complicaciones.</a> </p>
</p>

<div align="center">
  <img alt="GitHub" src="https://img.shields.io/github/license/davidgasquez/datalia?style=flat-square">
  <img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/davidgasquez/datalia/ci.yml?style=flat-square">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/davidgasquez/datalia?style=flat-square">
</div>

<br>

Datalia es una plataforma de datos abiertos a nivel de España con el objetivo de unificar y armonizar información proveniente de diferentes fuentes.

## 💡 Principios

- **Transparencia**: Código, estándares, infraestructura, y datos, son públicos. Usa herramientas, estándares e infraestructuras abiertas, y comparte datos en [formatos accesibles](https://voltrondata.com/codex/a-new-frontier).
- **Modularidad**: Cada componente o dataset puede ser reemplazado, extendido o eliminado. El código funciona bien en muchos entornos (un portátil, un clúster, o desde el navegador) y puede desplegarse en distintos lugares.
- **Sin Rozamiento**: No preguntes, haz un fork y mejora el código, los modelos, o añade una nueva fuente de datos. Usa los datasets sin límites de API o cuotas.
- **Datos como Código**: Transformaciones declarativas trackeadas en `git`. Los datasets y sus transformaciones se publican para que otras personas puedan construir sobre ellos.
- **Pegamento**: Datalia es un puente entre herramientas y enfoques y no un estándar o una herramienta en sí misma. Se integra con otras herramientas y servicios.

## ⚙️ Configuración

Si quieres contribuir a Datalia, es fácil! Clona el repositorio y sigue estas instrucciones.

Cualquier problema que encuentres, no dudes en [abrir una issue](https:github.com/davidgasqyez/datalia/issues/new)!

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

Ahora, puedes ejecutar `make dev` para iniciar el servidor de Dagster de Datalia.

## 📦 Estructura

Datalia está compuesta por varios componentes:

- **Dagster**: Una herramienta que orquesta los pipelines de datos.
- **DuckDB**: Una base de datos en memoria para almacenar los datos.
- **dbt**: Una herramienta de transformación de datos con SQL.
- **Observable Framework**: Un generador de páginas web estáticas con el que publicamos la web de Datalia.
- **HuggingFace**: Plataforma donde publicamos los datasets.

## 📄 Licencia

Datalia es un proyecto de código abierto bajo la licencia [MIT](LICENSE).
