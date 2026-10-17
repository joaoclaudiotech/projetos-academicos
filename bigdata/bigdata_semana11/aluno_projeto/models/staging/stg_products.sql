select
    cast(product_id as integer) as product_id,
    trim(product_name) as product_name,
    trim(category) as category
from {{ source('raw', 'products') }}
