---
header: >
  <nav>
    <a href="/">Datalia</a>
  </nav>
---
# IPC

<div class="grid grid-cols-4">
<div class="card">

_Última actualización:  ${new Date(now).toLocaleDateString()}_

</div>
<div class="card">

_💾 [Descargar](https://huggingface.co/datasets/datonic/spain_ipc)_

</div>
</div>

## Descripción

Índice de Precios de Consumo (IPC) en España.
Es una medida estadística de la evolución de los precios de los bienes y servicios que consume la población residente en viviendas familiares en España.

| Columna      | Descripción                                      | Tipo     |
|--------------|--------------------------------------------------|----------|
| fecha        | Fecha de la observación.                         | date     |
| id_clase     | Identificador de la clase de bienes y servicios. | string   |
| nombre_clase | Nombre de la clase de bienes y servicios.        | string   |
| valor        | Valor del IPC.                                   | float    |

Datos extraídos de INE (Instituto Nacional de Estadística).

- [Inventario](https://www.ine.es/dyngs/IOE/es/operacion.htm?numinv=30138)
- [Informe Metodológico](https://www.ine.es/dynt3/metadatos/es/RespuestaDatos.htm?oe=30138)

## Explorador

<iframe
  src="https://huggingface.co/datasets/datonic/spain_ipc/embed/viewer/default/train"
  frameborder="0"
  width="100%"
  height="560px"
></iframe>
