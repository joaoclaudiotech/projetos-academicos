from __future__ import annotations
import concurrent.futures as futures
import statistics
import threading
import time
import httpx
import bentoml

FEATURES = [35, 24, 3, 12, 159.90]
N = 120
WORKERS = 12
local = threading.local()


def percentile(values, p):
    values = sorted(values)
    idx = min(len(values)-1, max(0, round((len(values)-1)*p)))
    return values[idx]


def call_fastapi(_):
    if not hasattr(local, "http"):
        local.http = httpx.Client(timeout=10)
    t0 = time.perf_counter()
    r = local.http.post("http://127.0.0.1:8000/predict", json={"features": FEATURES})
    r.raise_for_status()
    return (time.perf_counter()-t0)*1000


def call_bento(_):
    if not hasattr(local, "bento"):
        local.bento = bentoml.SyncHTTPClient("http://127.0.0.1:3000", timeout=10)
    t0 = time.perf_counter()
    local.bento.predict(payload={"features": FEATURES})
    return (time.perf_counter()-t0)*1000


def call_bento_adaptive(_):
    if not hasattr(local, "bento"):
        local.bento = bentoml.SyncHTTPClient("http://127.0.0.1:3000", timeout=10)
    t0 = time.perf_counter()
    local.bento.predict_adaptive(rows=[FEATURES])
    return (time.perf_counter()-t0)*1000


def run(label, fn):
    start = time.perf_counter()
    with futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        lat = list(ex.map(fn, range(N)))
    total = time.perf_counter()-start
    return {
        "servico": label,
        "requests": N,
        "workers": WORKERS,
        "req_s": round(N/total, 2),
        "media_ms": round(statistics.mean(lat), 2),
        "p50_ms": round(percentile(lat, .50), 2),
        "p95_ms": round(percentile(lat, .95), 2),
    }

print("=== BENCHMARK DIDÁTICO ===")
print("Mesma máquina, mesmo modelo, mesma entrada. Resultados variam por hardware.")
print("Deixe FastAPI em 8000 e BentoML em 3000 rodando antes deste script.\n")
for label, fn in [
    ("FastAPI", call_fastapi),
    ("BentoML normal", call_bento),
    ("BentoML adaptive", call_bento_adaptive),
]:
    try:
        print(run(label, fn))
    except Exception as exc:
        print({"servico": label, "ERRO": str(exc)})

print("\nInterpretação: throughput maior não significa automaticamente melhor sistema.")
print("Observe também p95 e explique o trade-off throughput x latência.")
