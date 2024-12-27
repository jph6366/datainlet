---
header: >
  <nav>
    <a href="/">Datania</a>
  </nav>
---
# Demanda de Energía Eléctrica

<div class="grid grid-cols-4">
<div class="card">

_Última actualización:  ${new Date(now).toLocaleDateString()}_

</div>
<div class="card">

_💾 [Descargar](https://huggingface.co/datasets/datania/demanda_energia_electrica)_

</div>
</div>

## Descripción

Datos históricos de la demanda de energía eléctrica en España desde 2014.
Proporciona información horaria sobre el consumo de energía eléctrica en el sistema eléctrico español, recopilada por Red Eléctrica de España (REE).

| Columna  | Descripción                                     | Tipo   |
| -------- | ----------------------------------------------- | ------ |
| datetime | Fecha y hora de la medición                     | fecha  |
| value    | Demanda de energía eléctrica en megavatios (MW) | número |

Datos extraídos de Red Eléctrica de España (REE).

- [Portal de datos de REE](https://www.ree.es/es/apidatos)

## Explorador

<iframe
  src="https://huggingface.co/datasets/datania/demanda_energia_electrica/embed/viewer/default/train"
  frameborder="0"
  width="100%"
  height="560px"
></iframe>
