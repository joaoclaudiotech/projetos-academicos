from pathlib import Path
import json
import subprocess
import sys
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from model_core import FEATURE_NAMES, load_model, predict_many, predict_one, validate_features


def ensure_model():
    model_path = ROOT / "models" / "churn_model.joblib"
    if not model_path.exists():
        subprocess.run([sys.executable, str(ROOT / "01_treinar_modelo.py")], cwd=ROOT, check=True)
    return model_path


def test_feature_contract():
    assert len(FEATURE_NAMES) == 5
    arr = validate_features([35, 24, 3, 12, 159.9])
    assert arr.shape == (5,)
    with pytest.raises(ValueError):
        validate_features([1, 2])


def test_training_creates_artifacts():
    path = ensure_model()
    assert path.exists()
    meta = json.loads((ROOT / "models" / "metadata.json").read_text(encoding="utf-8"))
    assert meta["features"] == FEATURE_NAMES
    assert 0 <= meta["accuracy_test"] <= 1
    assert 0 <= meta["f1_test"] <= 1


def test_predictions_have_expected_shape():
    ensure_model()
    model = load_model(ROOT / "models" / "churn_model.joblib")
    one = predict_one(model, [35, 24, 3, 12, 159.9])
    assert set(one) == {"prediction", "probability_churn", "risk"}
    assert one["prediction"] in (0, 1)
    assert 0 <= one["probability_churn"] <= 1
    rows = predict_many(model, [[35,24,3,12,159.9],[62,4,7,60,379.0]])
    assert len(rows) == 2


def test_batch_rejects_empty():
    ensure_model()
    model = load_model(ROOT / "models" / "churn_model.joblib")
    with pytest.raises(ValueError):
        predict_many(model, [])
