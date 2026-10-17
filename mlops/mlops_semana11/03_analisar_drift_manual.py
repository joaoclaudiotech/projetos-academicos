from pathlib import Path
import pandas as pd
from src.drift_core import analisar_dataset, salvar_json, resumo_html

Path("reports").mkdir(exist_ok=True)
ref = pd.read_csv("data/referencia.csv")
for nome, arquivo in [("estavel", "data/producao_estavel.csv"), ("drift", "data/producao_drift.csv")]:
    cur = pd.read_csv(arquivo)
    resumo = analisar_dataset(ref, cur)
    salvar_json(resumo, f"reports/manual_{nome}.json")
    Path(f"reports/manual_{nome}.html").write_text(resumo_html(nome, resumo), encoding="utf-8")
    print(f"\n=== {nome.upper()} ===")
    print(f"status={resumo['status']} | colunas_drift={resumo['colunas_com_drift']}/{resumo['total_colunas']} | share={resumo['share_drift']:.0%}")
    for r in resumo["resultados"]:
        marcador = "DRIFT" if r["drift"] else "OK"
        psi = "-" if r["psi"] is None else f"{r['psi']:.3f}"
        pv = "-" if r["p_value"] is None else f"{r['p_value']:.3g}"
        print(f"{marcador:5} {r['coluna']:<18} p={pv:<9} PSI={psi}")
