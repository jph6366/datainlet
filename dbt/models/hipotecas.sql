with source as (
    select * from {{ source('main', 'raw_hipotecas') }}
),

renamed as (
    select
        periodo as fecha,
        provincias as provincia,
        naturaleza_de_la_finca as tipo_finca,
        numero_de_hipotecas,
        importe_de_hipotecas
    from source
),

cleaned as (
    select
        fecha,
        provincia,
        tipo_finca,
        numero_de_hipotecas,
        importe_de_hipotecas
    from renamed
    order by fecha desc
)

select * from cleaned order by fecha desc
