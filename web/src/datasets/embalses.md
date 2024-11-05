---
header: >
  <nav>
    <a href="/">Datania</a>
  </nav>
---
# Embalses

<div class="grid grid-cols-4">
<div class="card">

_Última actualización:  ${new Date(now).toLocaleDateString()}_

</div>
<div class="card">

_💾 [Descargar](https://huggingface.co/datasets/datania/embalses)_

</div>
</div>

## Descripción

Datos históricos de los embalses de España desde 1988.
Proporciona información sobre el estado y niveles de los embalses españoles, recopilada por el Ministerio para la Transición Ecológica y el Reto Demográfico (MITECO).

| Columna                      | Descripción                                      | Tipo      |
|------------------------------|--------------------------------------------------|-----------|
| fecha                        | Fecha de la medición                             | fecha     |
| embalse                      | Nombre del embalse                               | texto     |
| cuenca                       | Nombre de la cuenca hidrográfica                 | texto     |
| agua_actual                  | Volumen actual de agua en hm³                    | número    |
| agua_total                   | Capacidad total de agua en hm³                   | número    |
| porcentaje_agua              | Porcentaje de llenado de agua                    | número    |
| energia_actual               | Energía actual en GWh                            | número    |
| energia_total                | Capacidad total de energía en GWh                | número    |
| porcentaje_energia           | Porcentaje de energía disponible                 | número    |
| uso                          | Uso principal del embalse                        | texto     |
| variacion_agua               | Variación del volumen de agua                    | número    |
| variacion_energia            | Variación de la energía                          | número    |
| variacion_porcentaje_agua    | Variación del porcentaje de agua                 | número    |
| variacion_porcentaje_energia | Variación del porcentaje de energía              | número    |
| estado_agua                  | Estado del nivel de agua                         | texto     |
| estado_energia               | Estado del nivel de energía                      | texto     |
| es_electrico                 | Indica si el embalse es hidroeléctrico           | booleano  |


Datos extraídos de MITECO (Ministerio para la Transición Ecológica y el Reto Demográfico).

- [Portal de datos](https://www.miteco.gob.es/es/agua/temas/evaluacion-de-los-recursos-hidricos/boletin-hidrologico.html)

## Explorador

<iframe
  src="https://huggingface.co/datasets/datania/embalses/embed/viewer/default/train"
  frameborder="0"
  width="100%"
  height="560px"
></iframe>
