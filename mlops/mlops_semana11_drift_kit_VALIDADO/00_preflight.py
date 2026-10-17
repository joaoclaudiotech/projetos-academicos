from __future__ import annotations
import importlib
import platform
import sys

REQ = {
    "numpy": "numpy",
    "pandas": "pandas",
    "scipy": "scipy",
    "matplotlib": "matplotlib",
    "evidently": "evidently",
}

print("=== PRE-FLIGHT · SEMANA 11 ===")
print("Python:", sys.version.split()[0], "|", platform.system())
ok = sys.version_info >= (3, 10)
print("[PASS] Python 3.10+" if ok else "[FAIL] Use Python 3.10 ou superior")
for nome, modulo in REQ.items():
    try:
        m = importlib.import_module(modulo)
        versao = getattr(m, "__version__", "instalado")
        print(f"[PASS] {nome}: {versao}")
    except Exception as e:
        ok = False
        print(f"[FAIL] {nome}: {type(e).__name__}")
if not ok:
    print("\nExecute: python -m pip install -r requirements.txt")
    raise SystemExit(1)
print("\nPRE-FLIGHT APROVADO")
