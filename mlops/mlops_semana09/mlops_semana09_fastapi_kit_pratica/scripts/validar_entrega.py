from __future__ import annotations
import json
import sys
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8000"

def call(path, method="GET", payload=None):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"raw": body}
        return exc.code, parsed

def check(ok, label, detail=""):
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {label}" + (f" -> {detail}" if detail else ""))
    return bool(ok)

def main():
    good = 0
    total = 0
    def run(cond, label, detail=""):
        nonlocal good, total
        total += 1
        if check(cond, label, detail):
            good += 1

    try:
        st, body = call("/health")
    except Exception as exc:
        print("Não foi possível acessar a API em http://127.0.0.1:8000")
        print("Confirme que o Terminal 1 está executando:")
        print("python -m uvicorn app.main:app --reload --port 8000")
        print("Erro:", exc)
        sys.exit(2)

    run(st == 200 and body.get("status") == "healthy", "GET /health", str(body))

    st, body = call("/model/info")
    run(st == 200 and len(body.get("features", [])) == 5, "GET /model/info", str(body.get("features")))

    valid = {
        "idade": 35,
        "meses_cliente": 24,
        "chamados_suporte": 3,
        "dias_sem_login": 12,
        "valor_mensal": 159.90
    }
    st, body = call("/predict", "POST", valid)
    run(st == 200 and "probability" in body, "POST /predict válido", str(body))

    invalid = dict(valid)
    invalid["idade"] = 5
    st, body = call("/predict", "POST", invalid)
    run(st == 422, "POST /predict inválido gera 422", f"HTTP {st}")

    batch = {"instancias": [
        valid,
        {**valid, "chamados_suporte": 8, "dias_sem_login": 45, "valor_mensal": 390.0},
        {**valid, "meses_cliente": 80, "chamados_suporte": 0, "dias_sem_login": 2, "valor_mensal": 89.0},
    ]}
    st, body = call("/predict/batch", "POST", batch)
    run(st == 200 and body.get("total_processado") == 3, "POST /predict/batch com 3 instâncias", str(body.get("total_processado")))

    st, body = call("/metrics")
    run(st == 200 and body.get("total_instancias_preditas", 0) >= 4, "GET /metrics", str(body))

    st, body = call("/openapi.json")
    paths = body.get("paths", {}) if st == 200 else {}
    expected = {"/health", "/model/info", "/predict", "/predict/batch", "/metrics"}
    run(st == 200 and expected.issubset(paths.keys()), "OpenAPI contém os 5 endpoints", ", ".join(sorted(paths.keys())))

    print(f"\nResultado: {good}/{total} verificações passaram.")
    if good != total:
        sys.exit(1)
    print("Projeto pronto para gerar as evidências finais.")

if __name__ == "__main__":
    main()
