from pathlib import Path
import ast
ROOT=Path(__file__).resolve().parents[1]

def test_service_uses_modern_bentoml_api():
    text=(ROOT/'service.py').read_text(encoding='utf-8')
    ast.parse(text)
    assert '@bentoml.service' in text
    assert '@bentoml.api' in text
    assert 'BentoModel("classificador_churn:latest")' in text
    assert 'bentoml.Service(' not in text
    assert '.to_runner(' not in text
