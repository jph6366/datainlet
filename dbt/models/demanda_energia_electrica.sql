with source as (
    select * from {{ source('main', 'raw_demanda_energia_electrica') }}
),

renamed as (
    select
        datetime,
        value,
        percentage
    from source
),

select * from renamed order by datetime desc
