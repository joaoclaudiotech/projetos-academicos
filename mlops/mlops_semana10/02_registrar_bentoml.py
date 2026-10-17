from __future__ import annotations
import bentoml
from model_core import load_model, load_metadata

model = load_model()
meta = load_metadata()

saved = bentoml.sklearn.save_model(
    "classificador_churn",
    model,
    labels={"disciplina": "mlops", "semana": "10", "framework": "sklearn"},
    metadata=meta,
)

print("=== MODELO REGISTRADO NO BENTOML MODEL STORE ===")
print("Tag:", saved.tag)
print("Caminho:", saved.path)
print("\nModelos locais encontrados:")
for item in bentoml.models.list():
    print(" -", item.tag)
print("\nPróximo passo: bentoml serve service:ChurnService --reload")
