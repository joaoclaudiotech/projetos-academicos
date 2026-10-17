-- Um teste singular deve retornar ZERO linhas para passar.
select order_date, receita_total
from {{ ref('fct_revenue_daily') }}
where receita_total < 0
