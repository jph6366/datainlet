with indicadores_nacionales as (
    select
        'Total Nacional' as provincia,
        Periodo as fecha,
        Variable as variable,
        Total as valor
    from {{ source('main', 'raw_hipotecas_indicadores_nacionales') }}
),

indicadores_por_provincia as (
    select
        Periodo as fecha,
        Provincias as provincia,
        "Tabla y Variable" as variable,
        Total as valor
    from {{ source('main', 'raw_hipotecas_indicadores_por_provincia') }}
)

select * from indicadores_nacionales
union all
select * from indicadores_por_provincia
