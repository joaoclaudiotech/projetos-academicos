from pathlib import Path
import duckdb
DB=Path(__file__).with_name('semana11.duckdb')
if not DB.exists(): raise SystemExit('Banco não encontrado. Rode preparar_banco.py primeiro.')
con=duckdb.connect(str(DB), read_only=True)
try:
    total=con.execute('select count(*) from analytics.fct_revenue_daily').fetchone()[0]
    rows=con.execute('select * from analytics.fct_revenue_daily order by receita_total desc limit 5').fetchall()
except Exception as e:
    raise SystemExit('Mart não encontrado ou incompleto. Rode dbt build --profiles-dir .\n'+str(e))
print('MART OK ✅')
print('Dias no mart:',total)
print('Top 5 dias por receita:')
for r in rows: print(r)
con.close()
