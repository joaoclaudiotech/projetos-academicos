from __future__ import annotations
import importlib
import platform
import sys
from pathlib import Path

REQUIRED = {
    "numpy": "2.5.3",
    "sklearn": "1.9.1",
    "bentoml": "1.4.39",
    "fastapi": "0.142.2",
    "uvicorn": "0.54.0",
    "httpx": None,
}

print("=== PRE-FLIGHT · MLOps Semana 10 ===")
print("Python:", sys.version.split()[0])
print("SO:", platform.platform())
print("Pasta:", Path.cwd())

ok = True
for module, expected in REQUIRED.items():
    try:
        mod = importlib.import_module(module)
        version = getattr(mod, "__version__", "(sem __version__)")
        status = "OK"
        if expected and version != expected:
            status = f"ATENÇÃO: esperado {expected}, encontrado {version}"
        print(f"[{status}] {module}: {version}")
    except Exception as exc:
        ok = False
        print(f"[FALHA] {module}: {exc}")

models = Path("models")
models.mkdir(exist_ok=True)
print("[OK] Pasta models disponível")

if not ok:
    print("\nAlguma dependência não está instalada. Execute:")
    print("python -m pip install -r requirements.txt")
    raise SystemExit(1)

print("\nPRE-FLIGHT APROVADO. Pode seguir para 01_treinar_modelo.py")
