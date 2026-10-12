
# scripts/create_model.py
# Script didático para gerar um model.pkl local.
# Assim a prática não depende de um modelo salvo nas semanas anteriores.

# Path cria pastas/caminhos de forma compatível com Windows, Linux e macOS.
from pathlib import Path

# joblib salva objetos Python grandes, como modelos scikit-learn.
import joblib

# make_classification cria um dataset sintético de classificação.
from sklearn.datasets import make_classification

# LogisticRegression será o modelo simples desta prática.
from sklearn.linear_model import LogisticRegression

# train_test_split separa treino e teste para mostrar uma métrica real.
from sklearn.model_selection import train_test_split

# accuracy_score mede acurácia no conjunto de teste.
from sklearn.metrics import accuracy_score


# Pasta raiz do projeto.
ROOT = Path(__file__).resolve().parents[1]

# Pasta onde o modelo será salvo.
MODELS_DIR = ROOT / "models"

# Cria a pasta models se ela ainda não existir.
MODELS_DIR.mkdir(exist_ok=True)

# Caminho final do model.pkl.
MODEL_PATH = MODELS_DIR / "model.pkl"

# Cria dados sintéticos com 10 features, para combinar com sample_request.json.
X, y = make_classification(
    n_samples=600,
    n_features=10,
    n_informative=6,
    n_redundant=2,
    n_classes=2,
    random_state=42,
)

# Separa treino e teste.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

# Cria o modelo.
model = LogisticRegression(max_iter=1000)

# Treina o modelo.
model.fit(X_train, y_train)

# Calcula predição no teste.
pred = model.predict(X_test)

# Calcula acurácia simples para evidência no terminal.
accuracy = accuracy_score(y_test, pred)

# Salva o modelo em models/model.pkl.
joblib.dump(model, MODEL_PATH)

# Mensagens que o aluno pode copiar como evidência.
print("Modelo treinado com sucesso.")
print(f"Arquivo salvo em: {MODEL_PATH}")
print(f"Features esperadas: {model.n_features_in_}")
print(f"Acurácia de teste: {accuracy:.3f}")
