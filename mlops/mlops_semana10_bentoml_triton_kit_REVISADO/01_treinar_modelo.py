from __future__ import annotations
from pathlib import Path
import json
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from model_core import FEATURE_NAMES

RNG = np.random.default_rng(42)
N = 800

idade = RNG.integers(18, 80, N)
meses_cliente = RNG.integers(0, 121, N)
chamados = np.clip(RNG.poisson(2.3, N), 0, 15)
dias_sem_login = RNG.integers(0, 91, N)
valor_mensal = RNG.uniform(39, 420, N)

# Regra sintética didática: gera um padrão aprendível, com 5% de ruído.
# Assim o foco continua sendo serving, sem criar uma métrica artificialmente perfeita.
logit = (
    -1.3
    + 0.040 * (dias_sem_login - 20)
    + 0.45 * (chamados - 2)
    - 0.015 * (meses_cliente - 24)
    + 0.0030 * (valor_mensal - 150)
    + 0.005 * (idade - 40)
)
prob = 1.0 / (1.0 + np.exp(-logit))
y = (prob >= 0.5).astype(int)
noise = RNG.random(N) < 0.05
y = np.where(noise, 1 - y, y)
X = np.column_stack([idade, meses_cliente, chamados, dias_sem_login, valor_mensal])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=7,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=1,
)
model.fit(X_train, y_train)
yp = model.predict(X_test)
accuracy = float(accuracy_score(y_test, yp))
f1 = float(f1_score(y_test, yp, zero_division=0))

out = Path("models")
out.mkdir(exist_ok=True)
joblib.dump(model, out / "churn_model.joblib")
metadata = {
    "model_name": "classificador_churn",
    "algorithm": "RandomForestClassifier",
    "dataset_rows": N,
    "features": FEATURE_NAMES,
    "accuracy_test": round(accuracy, 4),
    "f1_test": round(f1, 4),
    "random_state": 42,
}
(out / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

print("=== TREINO CONCLUÍDO ===")
print("Arquivo:", out / "churn_model.joblib")
print("Features:", FEATURE_NAMES)
print("Accuracy teste:", round(accuracy, 4))
print("F1 teste:", round(f1, 4))
print("Próximo passo: python 02_registrar_bentoml.py")
