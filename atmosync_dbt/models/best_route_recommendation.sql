
WITH ranked_routes AS (
    SELECT
        CONTAINER_ID,
        ROUTE_ID,
        EXPECTED_TEMPERATURE_C,
        TRAVEL_TIME_HOURS,
        TRANSPORT_COST_INR,
        CURRENT_CONTAINER_RISK,
        ROUTE_TEMPERATURE_RISK,

        ROW_NUMBER() OVER (
            PARTITION BY CONTAINER_ID
            ORDER BY
                CASE ROUTE_TEMPERATURE_RISK
                    WHEN 'LOW' THEN 1
                    WHEN 'MEDIUM' THEN 2
                    ELSE 3
                END,
                TRANSPORT_COST_INR ASC,
                TRAVEL_TIME_HOURS ASC
        ) AS ROUTE_RANK

    FROM {{ ref('route_comparison') }}
)

SELECT
    *,
    CASE
        WHEN ROUTE_RANK = 1 THEN 'RECOMMENDED'
        ELSE 'ALTERNATIVE'
    END AS RECOMMENDATION_STATUS

FROM ranked_routes
