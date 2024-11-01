with source as (
    select * from {{ source('main', 'raw_spain_water_reservoirs_data') }}
),

renamed as (
    select
        fecha,
        embalse_nombre as embalse,
        ambito_nombre as cuenca,
        agua_actual,
        agua_total,
        Porcentaje_Reserva as porcentaje_agua,
        energia_actual,
        energia_total,
        Porcentaje_Energia as porcentaje_energia,
        Uso as uso,
        Variacion_Reserva as variacion_agua,
        Variacion_Energia as variacion_energia,
        Variacion_Porcentaje as variacion_porcentaje_agua,
        Variacion_Porcentaje_Energia as variacion_porcentaje_energia,
        Estado_Porc as estado_agua,
        Estado_Porcentaje_Energia as estado_energia,
        electrico_flag as es_electrico
    from source
),

cleaned as (
    select
        fecha,
        embalse,
        cuenca,
        agua_actual,
        agua_total,
        porcentaje_agua,
        energia_actual,
        energia_total,
        porcentaje_energia,
        uso,
        variacion_agua,
        variacion_energia,
        variacion_porcentaje_agua,
        variacion_porcentaje_energia,
        estado_agua,
        estado_energia,
        es_electrico
    from renamed
    order by fecha desc
)

select * from cleaned order by fecha desc
