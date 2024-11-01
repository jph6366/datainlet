---
header: >
  <nav>
    <a href="/">datania</a>
  </nav>
---
# Hipotecas

<div class="grid grid-cols-4">
<div class="card">

_Última actualización:  ${new Date(now).toLocaleDateString()}_

</div>
<div class="card">

_💾 [Descargar](https://huggingface.co/datasets/datania/hipotecas)_

</div>
</div>

## Descripción

Estadística de hipotecas constituidas en España.
Proporciona mensualmente información sobre el número de hipotecas constituidas sobre bienes inmuebles y el capital prestado.

| Columna              | Descripción                                     | Tipo     |
|----------------------|-------------------------------------------------|----------|
| fecha                | Fecha de la observación.                        | date     |
| provincia            | Provincia donde se constituye la hipoteca.      | string   |
| tipo_finca           | Tipo de finca sobre la que se constituye.       | string   |
| numero_de_hipotecas  | Número de hipotecas constituidas.               | integer  |
| importe_de_hipotecas | Importe total de las hipotecas (en euros).      | integer  |

Datos extraídos de INE (Instituto Nacional de Estadística).

- [Inventario](https://www.ine.es/dyngs/IOE/es/operacion.htm?numinv=30149)
- [Informe Metodológico](https://www.ine.es/dynt3/metadatos/es/RespuestaDatos.html?oe=30149)

## Explorador

<iframe
  src="https://huggingface.co/datasets/datania/hipotecas/embed/viewer/default/train"
  frameborder="0"
  width="100%"
  height="560px"
></iframe>
