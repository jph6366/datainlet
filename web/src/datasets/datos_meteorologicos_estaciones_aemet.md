---
header: >
  <nav>
    <a href="/">Datania</a>
  </nav>
---
# Datos Meteorológicos AEMET

<div class="grid grid-cols-4">
<div class="card">

_Última actualización:  ${new Date(now).toLocaleDateString()}_

</div>
<div class="card">

_💾 [Descargar](https://huggingface.co/datasets/datania/datos_meteorologicos_estaciones_aemet)_

</div>
</div>

## Descripción

Datos meteorológicos históricos de todas las estaciones meteorológicas de AEMET en España desde 1920.
Proporciona información diaria sobre temperatura, precipitación, viento y otros parámetros meteorológicos.

| Columna    | Descripción                              | Tipo   |
| ---------- | ---------------------------------------- | ------ |
| fecha      | Fecha de la medición                     | fecha  |
| indicativo | Código identificativo de la estación     | texto  |
| nombre     | Nombre de la estación meteorológica      | texto  |
| provincia  | Provincia donde se encuentra la estación | texto  |
| altitud    | Altitud de la estación en metros         | número |
| tmed       | Temperatura media diaria (°C)            | número |
| prec       | Precipitación diaria (mm)                | número |
| tmin       | Temperatura mínima diaria (°C)           | número |
| tmax       | Temperatura máxima diaria (°C)           | número |
| dir        | Dirección del viento                     | texto  |
| velmedia   | Velocidad media del viento (km/h)        | número |
| racha      | Racha máxima del viento (km/h)           | número |
| presMax    | Presión atmosférica máxima (hPa)         | número |
| presMin    | Presión atmosférica mínima (hPa)         | número |

Datos extraídos de AEMET (Agencia Estatal de Meteorología).

- [Portal de datos de AEMET](https://opendata.aemet.es/)

## Explorador

<iframe
  src="https://huggingface.co/datasets/datania/datos_meteorologicos_estaciones_aemet/embed/viewer/default/train"
  frameborder="0"
  width="100%"
  height="560px"
></iframe>
