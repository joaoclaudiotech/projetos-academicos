from __future__ import annotations
import json
import math
from pathlib import Path
from typing import Iterable

FEATURE_NAMES = [
    "idade",
    "meses_cliente",
    "chamados_suporte",
    "dias_sem_login",
    "valor_mensal",
]

class ChurnModel:
    """Modelo logístico didático salvo em JSON.

    Mantemos a classe pequena para que a aula foque serving/MLOps,
    sem depender de scikit-learn para executar a API.
    """
    def __init__(self, weights: list[float], bias: float, threshold: float = 0.5,
                 version: str = "1.0.0", metrics: dict | None = None):
        self.weights = weights
        self.bias = bias
        self.threshold = threshold
        self.version = version
        self.metrics = metrics or {}

    @staticmethod
    def _sigmoid(z: float) -> float:
        z = max(min(z, 40.0), -40.0)
        return 1.0 / (1.0 + math.exp(-z))

    def predict_proba_one(self, features: Iterable[float]) -> float:
        xs = list(features)
        if len(xs) != len(self.weights):
            raise ValueError(f"Esperadas {len(self.weights)} features; recebidas {len(xs)}.")
        z = self.bias + sum(w * x for w, x in zip(self.weights, xs))
        return self._sigmoid(z)

    def predict_one(self, features: Iterable[float]) -> tuple[int, float]:
        p = self.predict_proba_one(features)
        return int(p >= self.threshold), p

    def predict_many(self, rows: Iterable[Iterable[float]]) -> list[tuple[int, float]]:
        """Interface batch: uma chamada ao modelo recebe várias instâncias."""
        return [self.predict_one(row) for row in rows]

    @classmethod
    def load(cls, path: str | Path) -> "ChurnModel":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        return cls(
            weights=data["weights"],
            bias=data["bias"],
            threshold=data.get("threshold", 0.5),
            version=data.get("version", "1.0.0"),
            metrics=data.get("metrics", {}),
        )
