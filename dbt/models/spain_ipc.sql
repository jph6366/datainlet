with source as (
    select * from {{ source('public', 'raw_spain_ipc') }}
),

renamed as (
    select
        {{ adapter.quote("Clases") }} as class,
        {{ adapter.quote("Tipo de dato") }} as type,
        {{ adapter.quote("Periodo") }} as date,
        {{ adapter.quote("Total") }} as value
    from source
),

parsed as (
    select
        cast(strptime(REPLACE(date, 'M', '-'), '%Y-%m') as date) AS date,
        class,
        type,
        try_cast(replace(value, ',', '.') AS FLOAT) AS value,
    from renamed
),

cleaned as (
    select
        date,
        case
            when class != 'Índice general' then split_part(class, ' ', 1)
            else '0000'
        end as class_id,
        case
            when class != 'Índice general' then substring(class from position(' ' in class) + 1)
            else 'Índice general'
        end as class_name,
        value
    from parsed
    where type = 'Índice'
    order by date desc
)

select * from cleaned order by date desc
