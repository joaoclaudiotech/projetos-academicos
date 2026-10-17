from pathlib import Path
import json
import subprocess
import sys

checks = []
def check(nome, cond, detalhe=""):
    checks.append((nome, bool(cond), detalhe))

for p in ["data/referencia.csv", "data/producao_estavel.csv", "data/producao_drift.csv"]:
    check(f"arquivo {p}", Path(p).exists())
for p in ["reports/distribuicao_dias_sem_login.png", "reports/distribuicao_valor_mensal.png"]:
    check(f"gráfico {p}", Path(p).exists() and Path(p).stat().st_size > 1000)

p_ok = Path("reports/manual_estavel.json")
p_dr = Path("reports/manual_drift.json")
check("resumo manual estável", p_ok.exists())
check("resumo manual drift", p_dr.exists())
if p_ok.exists() and p_dr.exists():
    ok = json.loads(p_ok.read_text(encoding="utf-8"))
    dr = json.loads(p_dr.read_text(encoding="utf-8"))
    check("produção estável classificada ESTAVEL", ok.get("status") == "ESTAVEL", str(ok.get("status")))
    check("produção alterada classificada ALERTA", dr.get("status") == "ALERTA", str(dr.get("status")))
    check("drift detectado em >=3 colunas", dr.get("colunas_com_drift", 0) >= 3, str(dr.get("colunas_com_drift")))

# Evidently é requisito da atividade final: checa os relatórios se o aluno já executou a etapa.
for p in ["reports/evidently_estavel.html", "reports/evidently_drift.html"]:
    check(f"Evidently {p}", Path(p).exists() and Path(p).stat().st_size > 1000, "execute 04_relatorios_evidently.py se faltar")

print("=== VALIDAÇÃO DA ENTREGA ===")
for nome, passou, detalhe in checks:
    print(("[PASS]" if passou else "[FAIL]"), nome, (f"-> {detalhe}" if detalhe else ""))
n = sum(p for _, p, _ in checks)
print(f"\nResultado: {n}/{len(checks)} verificações passaram.")
raise SystemExit(0 if n == len(checks) else 1)
