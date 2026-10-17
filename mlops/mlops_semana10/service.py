from __future__ import annotations
import numpy as np
import bentoml
from pydantic import BaseModel, Field
from model_core import FEATURE_NAMES, predict_many, predict_one

# API MODERNA do BentoML 1.4.x: Service baseado em classe.
# A imagem descreve o ambiente que será usado quando o Bento for empacotado/containerizado.
image = (
    bentoml.images.Image(python_version="3.12")
    .python_packages("scikit-learn==1.9.1", "numpy==2.5.3")
)


class PredictionRequest(BaseModel):
    features: list[float] = Field(
        min_length=5,
        max_length=5,
        description=f"Ordem obrigatória: {FEATURE_NAMES}",
        examples=[[35, 24, 3, 12, 159.90]],
    )


class PredictionResponse(BaseModel):
    prediction: int
    probability_churn: float
    risk: str


@bentoml.service(
    name="servico_churn",
    image=image,
    traffic={"timeout": 10},
)
class ChurnService:
    # IMPORTANTE: referência no escopo da classe para o Bento rastrear o modelo como dependência.
    model_ref = bentoml.models.BentoModel("classificador_churn:latest")

    def __init__(self) -> None:
        self.model = bentoml.sklearn.load_model(self.model_ref)

    @bentoml.api(route="/predict")
    def predict(self, payload: PredictionRequest) -> PredictionResponse:
        result = predict_one(self.model, payload.features)
        return PredictionResponse(**result)

    @bentoml.api(route="/predict_batch")
    def predict_batch(self, rows: list[list[float]]) -> list[dict]:
        return predict_many(self.model, rows)

    # Adaptive batching: o servidor pode juntar chamadas concorrentes.
    # Cada chamada envia rows=[[f1,f2,f3,f4,f5]].
    @bentoml.api(
        route="/predict_adaptive",
        batchable=True,
        max_batch_size=16,
        max_latency_ms=50,
    )
    def predict_adaptive(self, rows: list[list[float]]) -> list[int]:
        X = np.vstack(rows).astype(float)
        if X.ndim != 2 or X.shape[1] != 5:
            raise ValueError(f"Esperado array Nx5. Ordem: {FEATURE_NAMES}")
        return [int(v) for v in self.model.predict(X)]
