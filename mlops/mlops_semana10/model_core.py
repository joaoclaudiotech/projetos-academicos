from __future__ import annotations
from pathlib import Path
import json
import joblib
import numpy as np

FEATURE_NAMES = [
    "idade",
    "meses_cliente",
    "chamados_suporte",
    "dias_sem_login",
    "valor_mensal",
]
MODEL_PATH = Path(__file__).parent / "models" / "churn_model.joblib"
META_PATH = Path(__file__).parent / "models" / "metadata.json"


def load_model(path: Path | None = None):
    target = path or MODEL_PATH
    if not target.exists():
        raise FileNotFoundError(
            f"Modelo não encontrado em {target}. Rode: python 01_treinar_modelo.py"
        )
    return joblib.load(target)


def load_metadata(path: Path | None = None) -> dict:
    target = path or META_PATH
    if not target.exists():
        return {}
    return json.loads(target.read_text(encoding="utf-8"))


def validate_features(features: list[float] | tuple[float, ...]) -> np.ndarray:
    if len(features) != len(FEATURE_NAMES):
        raise ValueError(
            f"Esperadas {len(FEATURE_NAMES)} features na ordem {FEATURE_NAMES}; "
            f"recebidas {len(features)}."
        )
    arr = np.asarray(features, dtype=float)
    if not np.isfinite(arr).all():
        raise ValueError("Todas as features devem ser números finitos.")
    return arr


def predict_one(model, features) -> dict:
    arr = validate_features(features).reshape(1, -1)
    pred = int(model.predict(arr)[0])
    if hasattr(model, "predict_proba"):
        proba = float(model.predict_proba(arr)[0][1])
    else:
        proba = float(pred)
    return {
        "prediction": pred,
        "probability_churn": round(proba, 4),
        "risk": "alto" if proba >= 0.5 else "baixo",
    }


def predict_many(model, rows: list[list[float]]) -> list[dict]:
    if not rows:
        raise ValueError("O lote não pode ser vazio.")
    X = np.vstack([validate_features(row) for row in rows])
    preds = model.predict(X)
    if hasattr(model, "predict_proba"):
        probas = model.predict_proba(X)[:, 1]
    else:
        probas = preds.astype(float)
    return [
        {
            "prediction": int(pred),
            "probability_churn": round(float(proba), 4),
            "risk": "alto" if float(proba) >= 0.5 else "baixo",
        }
        for pred, proba in zip(preds, probas)
    ]
