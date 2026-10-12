from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel, Field
from model_core import FEATURE_NAMES, load_model, predict_one

MODEL = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global MODEL
    MODEL = load_model()
    yield

app = FastAPI(title="Baseline FastAPI · Semana 10", version="1.0", lifespan=lifespan)

class PredictionRequest(BaseModel):
    features: list[float] = Field(min_length=5, max_length=5, description=f"Ordem: {FEATURE_NAMES}")

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": MODEL is not None}

@app.post("/predict")
def predict(payload: PredictionRequest):
    return predict_one(MODEL, payload.features)
