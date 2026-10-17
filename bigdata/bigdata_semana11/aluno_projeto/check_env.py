from pathlib import Path
import subprocess, sys
print('Python:', sys.version.split()[0])
if sys.version_info < (3,10):
    raise SystemExit('ERRO: use Python 3.10 ou superior.')
try:
    import duckdb
    print('DuckDB:', duckdb.__version__)
except Exception:
    raise SystemExit('ERRO: DuckDB/dbt ainda não instalado. Rode: python -m pip install -r requirements.txt')
try:
    r = subprocess.run(['dbt','--version'], capture_output=True, text=True, timeout=30)
except FileNotFoundError:
    raise SystemExit('ERRO: comando dbt não encontrado. Rode: python -m pip install -r requirements.txt')
if r.returncode != 0:
    raise SystemExit('ERRO ao executar dbt --version:\n'+r.stderr)
print(r.stdout.splitlines()[0] if r.stdout else 'dbt encontrado')
required=['dbt_project.yml','profiles.yml','models/sources.yml','models/staging/stg_orders.sql','models/marts/fct_revenue_daily.sql']
missing=[x for x in required if not Path(x).exists()]
if missing: raise SystemExit('ERRO: arquivos ausentes: '+', '.join(missing))
print('AMBIENTE OK ✅')
