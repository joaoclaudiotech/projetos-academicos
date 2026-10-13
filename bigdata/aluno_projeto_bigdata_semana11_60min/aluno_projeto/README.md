# Semana 11 — ETL/ELT + dbt (60 min)

Projeto já configurado para **dbt Core + DuckDB**. Não rode `dbt init`.

## Sequência
1. `python -m pip install -r requirements.txt`
2. `python check_env.py`
3. `python preparar_banco.py`
4. `dbt debug --profiles-dir .`
5. Siga o caderno para observar a falha, corrigir TODO 1 e TODO 2.
6. `dbt build --profiles-dir .`
7. `python verificar_resultado.py`

> O projeto usa `profiles.yml` dentro da própria pasta para evitar configuração em `~/.dbt`.
