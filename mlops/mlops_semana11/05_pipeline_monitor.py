from __future__ import annotations
from datetime import datetime
from pathlib import Path
import argparse
import pandas as pd
from src.drift_core import analisar_dataset, salvar_json

parser = argparse.ArgumentParser()
parser.add_argument("--dataset", choices=["estavel", "drift"], default="drift")
args = parser.parse_args()

ref = pd.read_csv("data/referencia.csv")
cur_path = "data/producao_estavel.csv" if args.dataset == "estavel" else "data/producao_drift.csv"
cur = pd.read_csv(cur_path)
resumo = analisar_dataset(ref, cur)

ts = datetime.now().strftime("%Y%m%d_%H%M%S")
Path("reports/historico").mkdir(parents=True, exist_ok=True)
out = Path("reports/historico") / f"monitor_{args.dataset}_{ts}.json"
salvar_json({"timestamp": ts, "dataset": args.dataset, **resumo}, out)

print("=== MONITORAMENTO AUTOMATIZADO ===")
print("dataset:", args.dataset)
print("status:", resumo["status"])
print("drift:", f"{resumo['colunas_com_drift']}/{resumo['total_colunas']}", f"({resumo['share_drift']:.0%})")
print("historico:", out)
if resumo["status"] == "ALERTA":
    print("AÇÃO: investigar origem da mudança; não retreinar automaticamente sem diagnóstico.")
else:
    print("AÇÃO: manter monitoramento; nenhuma ação corretiva imediata.")
