from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from fastapi.testclient import TestClient
import fastapi_baseline


def setup_module():
    if not (ROOT/'models'/'churn_model.joblib').exists():
        subprocess.run([sys.executable, str(ROOT/'01_treinar_modelo.py')], cwd=ROOT, check=True)


def test_fastapi_health_and_predict():
    with TestClient(fastapi_baseline.app) as client:
        assert client.get('/health').status_code == 200
        r=client.post('/predict', json={'features':[35,24,3,12,159.9]})
        assert r.status_code == 200
        data=r.json()
        assert data['prediction'] in (0,1)
        bad=client.post('/predict', json={'features':[1,2]})
        assert bad.status_code == 422
