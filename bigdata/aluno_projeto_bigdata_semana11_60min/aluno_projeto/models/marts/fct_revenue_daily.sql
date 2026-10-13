-- TODO 2: substitua este modelo simples pelo mart do caderno.
select
    order_date,
    count(order_id) as total_pedidos,
    round(sum(total), 2) as receita_total,
    round(avg(total), 2) as ticket_medio
from {{ ref('stg_orders') }}
where status = 'paid'
group by order_date