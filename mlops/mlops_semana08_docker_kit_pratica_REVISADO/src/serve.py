
# src/serve.py
# API mínima de inferência com FastAPI.
# Este arquivo é executado dentro do container Docker pelo comando uvicorn.

# Path ajuda a montar caminhos de arquivo independentes do sistema operacional.
from pathlib import Path

# List permite declarar que a entrada será uma lista de números.
from typing import List

# joblib carrega o modelo treinado salvo em models/model.pkl.
import joblib

# numpy transforma a lista recebida em array no formato esperado pelo modelo.
import numpy as np

# FastAPI cria a aplicação web; HTTPException devolve erro HTTP controlado.
from fastapi import FastAPI, HTTPException

# BaseModel valida JSON de entrada e saída.
from pydantic import BaseModel, Field


# Cria a aplicação FastAPI e configura título/versão para a documentação automática.
app = FastAPI(
    title="Modelo de Inferência",
    version="1.0.0",
    description="API de inferência empacotada com Docker para a Semana 8 de MLOps.",
)

# Caminho absoluto para a pasta raiz do projeto dentro do container.
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Caminho esperado do modelo dentro do container.
MODEL_PATH = PROJECT_ROOT / "models" / "model.pkl"

# Se o modelo não existir, falhamos cedo com uma mensagem clara.
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Modelo não encontrado em {MODEL_PATH}. "
        "Execute scripts/create_model.py antes do build ou verifique a pasta models/."
    )

# Carrega o modelo uma única vez na inicialização da API.
MODEL = joblib.load(MODEL_PATH)

# Descobre quantas features o modelo espera.
EXPECTED_FEATURES = int(getattr(MODEL, "n_features_in_", 10))


# Modelo de entrada: JSON precisa ter uma chave "features" com lista de números.
class InputData(BaseModel):
    # Field adiciona descrição para aparecer em /docs.
    features: List[float] = Field(
        ...,
        description=f"Lista com {EXPECTED_FEATURES} valores numéricos.",
        example=[0.5, -1.2, 0.8, 1.1, -0.3, 0.6, 1.5, -0.9, 0.2, 0.7],
    )


# Modelo de saída: deixa o retorno previsível para quem consome a API.
class Prediction(BaseModel):
    # Classe prevista pelo modelo.
    prediction: int

    # Probabilidade da classe prevista.
    probability: float

    # Quantidade de features recebidas, útil para debug em aula.
    features_received: int

    # Nome da classe Python do modelo carregado.
    model_type: str


# Endpoint simples para saber se o container está vivo.
@app.get("/")
def health():
    # Retorna um JSON pequeno para curl ou navegador.
    return {
        "status": "ok",
        "model_type": type(MODEL).__name__,
        "expected_features": EXPECTED_FEATURES,
    }


# Endpoint de predição.
@app.post("/predict", response_model=Prediction)
def predict(data: InputData):
    # Valida se a quantidade de features bate com o que o modelo espera.
    if len(data.features) != EXPECTED_FEATURES:
        raise HTTPException(
            status_code=400,
            detail=f"Esperado {EXPECTED_FEATURES} features, recebido {len(data.features)}.",
        )

    # Transforma a lista em matriz com 1 linha e N colunas.
    X = np.array(data.features, dtype=float).reshape(1, -1)

    # Calcula a classe prevista.
    pred = int(MODEL.predict(X)[0])

    # Se o modelo tiver predict_proba, usamos a probabilidade real.
    if hasattr(MODEL, "predict_proba"):
        # Lista das classes aprendidas pelo modelo.
        classes = list(MODEL.classes_)

        # Índice da classe prevista dentro do vetor de probabilidades.
        pred_index = classes.index(pred)

        # Probabilidade da classe prevista.
        probability = float(MODEL.predict_proba(X)[0][pred_index])
    else:
        # Fallback didático para modelos sem probabilidade.
        probability = 1.0

    # Retorna objeto validado pelo Pydantic.
    return Prediction(
        prediction=pred,
        probability=probability,
        features_received=len(data.features),
        model_type=type(MODEL).__name__,
    )
