"""Gera relatórios com a API atual do Evidently 0.7.x.
API de referência: from evidently import Report; from evidently.presets import DataDriftPreset.
"""
from pathlib import Path
import pandas as pd

try:
    import evidently
    from evidently import Report
    from evidently.presets import DataDriftPreset
except Exception as exc:
    print("[ERRO] Evidently não está disponível neste ambiente.")
    print("Execute: python -m pip install -r requirements.txt")
    print("Detalhe:", repr(exc))
    raise SystemExit(2)

print("Evidently:", getattr(evidently, "__version__", "versão não exposta"))
Path("reports").mkdir(exist_ok=True)
ref = pd.read_csv("data/referencia.csv")

for nome, arquivo in [("estavel", "data/producao_estavel.csv"), ("drift", "data/producao_drift.csv")]:
    cur = pd.read_csv(arquivo)
    # Na API atual, testes podem ser incorporados ao próprio Report.
    report = Report([DataDriftPreset()], include_tests=True)
    snapshot = report.run(cur, ref)
    html = Path("reports") / f"evidently_{nome}.html"
    js = Path("reports") / f"evidently_{nome}.json"
    snapshot.save_html(str(html))
    js.write_text(snapshot.json(), encoding="utf-8")
    print(f"[OK] {html}")
    print(f"[OK] {js}")
