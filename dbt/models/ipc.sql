with source as (
    select * from {{ source('main', 'raw_ipc') }}
),

renamed as (
    select
        {{ adapter.quote("Clases") }} as clase,
        {{ adapter.quote("Tipo de dato") }} as tipo_de_dato,
        {{ adapter.quote("Periodo") }} as fecha,
        {{ adapter.quote("Total") }} as value
    from source
),

parsed as (
    select
        cast(strptime(REPLACE(fecha, 'M', '-'), '%Y-%m') as date) AS fecha,
        clase,
        tipo_de_dato,
        try_cast(replace(value, ',', '.') AS FLOAT) AS valor,
    from renamed
),

cleaned as (
    select
        fecha,
        case
            when clase != 'Índice general' then split_part(clase, ' ', 1)
            else '0000'
        end as id_clase,
        case
            when clase != 'Índice general' then substring(clase from position(' ' in clase) + 1)
            else 'Índice general'
        end as nombre_clase,
        valor
    from parsed
    where tipo_de_dato = 'Índice'
    order by fecha desc
)

select * from cleaned order by fecha desc
