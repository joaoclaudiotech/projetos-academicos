from __future__ import annotations
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "model.json"

FEATURE_NAMES = [
    "idade",
    "meses_cliente",
    "chamados_suporte",
    "dias_sem_login",
    "valor_mensal",
]

# Escalas deixam as variáveis em ordens de grandeza parecidas.
SCALES = [100.0, 120.0, 10.0, 60.0, 500.0]

def sigmoid(z: float) -> float:
    z = max(min(z, 40.0), -40.0)
    return 1.0 / (1.0 + math.exp(-z))

def make_dataset(n: int = 420, seed: int = 42):
    rng = random.Random(seed)
    rows = []
    for _ in range(n):
        idade = rng.randint(18, 78)
        meses = rng.randint(1, 120)
        chamados = rng.randint(0, 10)
        dias = rng.randint(0, 60)
        valor = round(rng.uniform(40, 450), 2)

        # Regra oculta que gera o rótulo sintético.
        logit = (
            -2.4
            + 0.42 * chamados
            + 0.055 * dias
            + 0.0035 * valor
            - 0.018 * meses
            - 0.006 * idade
        )
        prob = sigmoid(logit)
        y = 1 if rng.random() < prob else 0
        rows.append(([idade, meses, chamados, dias, valor], y))
    return rows

def train(rows, epochs: int = 1800, lr: float = 0.18):
    weights = [0.0] * len(FEATURE_NAMES)
    bias = 0.0

    for _ in range(epochs):
        dw = [0.0] * len(weights)
        db = 0.0
        for x_raw, y in rows:
            x = [v / s for v, s in zip(x_raw, SCALES)]
            p = sigmoid(bias + sum(w * v for w, v in zip(weights, x)))
            err = p - y
            db += err
            for j in range(len(weights)):
                dw[j] += err * x[j]
        m = len(rows)
        bias -= lr * db / m
        for j in range(len(weights)):
            weights[j] -= lr * dw[j] / m

    # Converter pesos treinados em variáveis escaladas para pesos nas variáveis originais.
    raw_weights = [w / s for w, s in zip(weights, SCALES)]
    return raw_weights, bias

def accuracy(rows, weights, bias, threshold=0.5):
    correct = 0
    for x, y in rows:
        p = sigmoid(bias + sum(w * v for w, v in zip(weights, x)))
        pred = int(p >= threshold)
        correct += int(pred == y)
    return correct / len(rows)

def main():
    rows = make_dataset()
    split = int(len(rows) * 0.8)
    train_rows = rows[:split]
    test_rows = rows[split:]
    weights, bias = train(train_rows)
    acc = accuracy(test_rows, weights, bias)

    payload = {
        "model_type": "logistic_regression_didatica",
        "version": "1.0.0",
        "feature_names": FEATURE_NAMES,
        "weights": [round(v, 8) for v in weights],
        "bias": round(bias, 8),
        "threshold": 0.5,
        "metrics": {"accuracy_sintetica": round(acc, 4), "n_train": len(train_rows), "n_test": len(test_rows)},
    }
    MODEL_PATH.parent.mkdir(exist_ok=True)
    MODEL_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    print("OK - modelo treinado")
    print(f"Arquivo: {MODEL_PATH}")
    print(f"Features: {len(FEATURE_NAMES)} -> {', '.join(FEATURE_NAMES)}")
    print(f"Acurácia sintética de teste: {acc:.3f}")

if __name__ == "__main__":
    main()
