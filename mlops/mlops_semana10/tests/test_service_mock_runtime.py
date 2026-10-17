from pathlib import Path
import importlib.util
import sys
import types

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from model_core import load_model

class FakeImage:
    def __init__(self,*a,**k): pass
    def python_packages(self,*a,**k): return self

class FakeBentoModel:
    def __init__(self,tag): self.tag=tag

fake=types.ModuleType('bentoml')
fake.images=types.SimpleNamespace(Image=FakeImage)
fake.models=types.SimpleNamespace(BentoModel=FakeBentoModel)
fake.sklearn=types.SimpleNamespace(load_model=lambda ref: load_model(ROOT/'models'/'churn_model.joblib'))
def service(*args,**kwargs):
    if args and isinstance(args[0],type) and len(args)==1 and not kwargs: return args[0]
    return lambda cls: cls
def api(*args,**kwargs):
    if args and callable(args[0]) and len(args)==1 and not kwargs: return args[0]
    return lambda fn: fn
fake.service=service
fake.api=api
sys.modules['bentoml']=fake

spec=importlib.util.spec_from_file_location('service_under_test', ROOT/'service.py')
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def test_service_methods_with_framework_stub():
    svc=mod.ChurnService()
    out=svc.predict(mod.PredictionRequest(features=[35,24,3,12,159.9]))
    assert out.prediction in (0,1)
    assert 0 <= out.probability_churn <= 1
    batch=svc.predict_batch([[35,24,3,12,159.9],[62,4,7,60,379.0]])
    assert len(batch)==2
    adaptive=svc.predict_adaptive([[35,24,3,12,159.9],[62,4,7,60,379.0]])
    assert len(adaptive)==2
