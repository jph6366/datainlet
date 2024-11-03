with source as (
    select * from {{ source('main', 'raw_hipotecas') }}
),

renamed as (
    select
        Periodo as fecha,
        Provincias as provincia,
        "Tabla y Variable" as variable,
        Total as valor
    from source
),

cleaned as (
    select
        fecha,
        provincia,
        variable,
        valor
    from renamed
    order by fecha desc
)

select * from cleaned order by fecha desc
