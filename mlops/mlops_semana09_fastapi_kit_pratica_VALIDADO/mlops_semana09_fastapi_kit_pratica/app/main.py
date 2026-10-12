from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

from app.model import ChurnModel, FEATURE_NAMES

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "model.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("api-churn")

STATE = {
    "model": None,
    "predicoes_individuais": 0,
    "instancias_batch": 0,
}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carrega o modelo uma vez antes de atender requisições."""
    try:
        STATE["model"] = ChurnModel.load(MODEL_PATH)
        logger.info("Modelo carregado: %s", MODEL_PATH)
    except Exception as exc:
        STATE["model"] = None
        logger.exception("Falha ao carregar modelo: %s", exc)
    yield
    STATE["model"] = None

app = FastAPI(
    title="API de Churn — Semana 09 MLOps",
    description="API didática para serving de modelo: validação, single, batch, docs e observabilidade básica.",
    version="1.0.0",
    lifespan=lifespan,
)

class PredictionInput(BaseModel):
    idade: int = Field(ge=18, le=100, description="Idade do cliente em anos", examples=[35])
    meses_cliente: int = Field(ge=0, le=180, description="Tempo como cliente, em meses", examples=[24])
    chamados_suporte: int = Field(ge=0, le=30, description="Chamados recentes ao suporte", examples=[3])
    dias_sem_login: int = Field(ge=0, le=365, description="Dias desde o último login", examples=[12])
    valor_mensal: float = Field(ge=0, le=5000, description="Valor mensal do contrato", examples=[159.9])

    def as_features(self) -> list[float]:
        return [
            float(self.idade),
            float(self.meses_cliente),
            float(self.chamados_suporte),
            float(self.dias_sem_login),
            float(self.valor_mensal),
        ]

class PredictionOutput(BaseModel):
    prediction: int = Field(description="0 = permanece, 1 = risco de churn")
    probability: float = Field(ge=0, le=1)
    risco: str
    modelo_versao: str
    tempo_inferencia_ms: float

class BatchInput(BaseModel):
    instancias: list[PredictionInput] = Field(min_length=1, max_length=100)

class BatchOutput(BaseModel):
    resultados: list[PredictionOutput]
    total_processado: int
    tempo_total_ms: float

def require_model() -> ChurnModel:
    model = STATE["model"]
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo não disponível. Execute o treino e reinicie a API.")
    return model

def make_output(model: ChurnModel, data: PredictionInput, tempo_ms: float) -> PredictionOutput:
    pred, proba = model.predict_one(data.as_features())
    return PredictionOutput(
        prediction=pred,
        probability=round(proba, 4),
        risco="alto" if pred == 1 else "baixo",
        modelo_versao=model.version,
        tempo_inferencia_ms=round(tempo_ms, 3),
    )

@app.middleware("http")
async def log_requests(request: Request, call_next):
    inicio = time.perf_counter()
    response = await call_next(request)
    duracao_ms = (time.perf_counter() - inicio) * 1000
    response.headers["X-Process-Time-Ms"] = f"{duracao_ms:.3f}"
    logger.info("%s %s status=%s tempo=%.2fms",
                request.method, request.url.path, response.status_code, duracao_ms)
    return response

@app.get("/health", tags=["operacao"], summary="Verifica se API e modelo estão prontos")
def health():
    if STATE["model"] is None:
        raise HTTPException(status_code=503, detail="API ativa, mas modelo não carregado")
    return {"status": "healthy", "modelo_carregado": True}

@app.get("/model/info", tags=["modelo"], summary="Metadados do modelo carregado")
def model_info():
    model = require_model()
    return {
        "tipo": "regressao_logistica_didatica",
        "versao": model.version,
        "features": FEATURE_NAMES,
        "threshold": model.threshold,
        "metricas_treino": model.metrics,
    }

@app.post("/predict", response_model=PredictionOutput, tags=["predicao"], summary="Predição individual")
def predict(data: PredictionInput):
    model = require_model()
    inicio = time.perf_counter()
    pred, proba = model.predict_one(data.as_features())
    tempo_ms = (time.perf_counter() - inicio) * 1000
    STATE["predicoes_individuais"] += 1
    return PredictionOutput(
        prediction=pred,
        probability=round(proba, 4),
        risco="alto" if pred == 1 else "baixo",
        modelo_versao=model.version,
        tempo_inferencia_ms=round(tempo_ms, 3),
    )

@app.post("/predict/batch", response_model=BatchOutput, tags=["predicao"], summary="Predição em lote")
def predict_batch(data: BatchInput):
    model = require_model()
    inicio = time.perf_counter()
    feature_rows = [item.as_features() for item in data.instancias]
    batch_predictions = model.predict_many(feature_rows)  # uma chamada de batch ao objeto de modelo
    total_ms = (time.perf_counter() - inicio) * 1000
    media_ms = total_ms / max(len(batch_predictions), 1)
    resultados = [
        PredictionOutput(
            prediction=pred,
            probability=round(proba, 4),
            risco="alto" if pred == 1 else "baixo",
            modelo_versao=model.version,
            tempo_inferencia_ms=round(media_ms, 3),
        )
        for pred, proba in batch_predictions
    ]
    STATE["instancias_batch"] += len(resultados)
    return BatchOutput(
        resultados=resultados,
        total_processado=len(resultados),
        tempo_total_ms=round(total_ms, 3),
    )

@app.get("/metrics", tags=["operacao"], summary="Contadores didáticos em memória")
def metrics():
    return {
        "predicoes_individuais": STATE["predicoes_individuais"],
        "instancias_batch": STATE["instancias_batch"],
        "total_instancias_preditas": STATE["predicoes_individuais"] + STATE["instancias_batch"],
        "observacao": "Contadores em memória: reiniciar a API zera os valores.",
    }

@app.get("/about", tags=["operacao"], summary="Identificação da implementação")
def about():
    return {
        "aluno": "João Cláudio",
        "disciplina": "MLOps",
        "semana": 9,
        "mensagem": "Minha primeira API de serving"
    }