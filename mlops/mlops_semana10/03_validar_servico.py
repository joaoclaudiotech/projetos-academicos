from __future__ import annotations
from pathlib import Path
import sys

FEATURES = [35, 24, 3, 12, 159.90]
ROWS = [FEATURES, [62, 4, 7, 60, 379.0], [28, 70, 0, 2, 79.0]]

def check(name, fn):
    try:
        value = fn()
        print(f"[PASS] {name}: {value}")
        return 1
    except Exception as exc:
        print(f"[FAIL] {name}: {type(exc).__name__}: {exc}")
        return 0

if not Path("models/churn_model.joblib").exists():
    print("[FAIL] Modelo local ausente. Rode 01_treinar_modelo.py")
    raise SystemExit(1)

try:
    import bentoml
except Exception as exc:
    print("[FAIL] BentoML não importou:", exc)
    raise SystemExit(1)

score = 0
score += check("BentoML versão", lambda: bentoml.__version__)
score += check("Model Store contém classificador_churn", lambda: [str(m.tag) for m in bentoml.models.list() if str(m.tag).startswith("classificador_churn:")][-1])

try:
    with bentoml.SyncHTTPClient("http://localhost:3000", server_ready_timeout=8) as client:
        score += check("POST predict", lambda: client.predict(payload={"features": FEATURES}))
        score += check("POST predict_batch", lambda: client.predict_batch(rows=ROWS))
        score += check("POST predict_adaptive", lambda: client.predict_adaptive(rows=[FEATURES]))
except Exception as exc:
    print("[FAIL] Não foi possível conectar ao BentoML em http://localhost:3000")
    print("       Deixe este comando rodando em outro terminal:")
    print("       bentoml serve service:ChurnService --reload")
    print("       Erro:", exc)

print(f"\nResultado: {score}/5 verificações passaram.")
if score < 5:
    raise SystemExit(1)
print("VALIDAÇÃO APROVADA.")
