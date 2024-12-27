---
header: >
  <nav>
    <a href="/">Datania</a>
  </nav>
---
# Estaciones AEMET

<div class="grid grid-cols-4">
<div class="card">

_Última actualización:  ${new Date(now).toLocaleDateString()}_

</div>
<div class="card">

_💾 [Descargar](https://huggingface.co/datasets/datania/estaciones_aemet)_

</div>
</div>

## Descripción

Datos de las estaciones meteorológicas de AEMET (Agencia Estatal de Meteorología) en España.
Proporciona información sobre la ubicación y características de todas las estaciones meteorológicas operadas por AEMET.

| Columna              | Descripción                                   | Tipo   |
| -------------------- | --------------------------------------------- | ------ |
| latitud              | Latitud de la estación en grados decimales    | número |
| longitud             | Longitud de la estación en grados decimales   | número |
| provincia            | Provincia donde se encuentra la estación      | texto  |
| indicativo           | Código identificativo de la estación          | texto  |
| nombre               | Nombre de la estación meteorológica           | texto  |
| indicativo_sinoptico | Código sinóptico internacional de la estación | texto  |

Datos extraídos de AEMET (Agencia Estatal de Meteorología).

- [Portal de datos de AEMET](https://opendata.aemet.es/)

## Explorador

<iframe
  src="https://huggingface.co/datasets/datania/estaciones_aemet/embed/viewer/default/train"
  frameborder="0"
  width="100%"
  height="560px"
></iframe>
