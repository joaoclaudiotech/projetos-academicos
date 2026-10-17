import pandas as pd
from src.drift_core import psi_numerico, analisar_dataset

def test_psi_identico_baixo():
    s = pd.Series(range(1, 101))
    assert psi_numerico(s, s) < 1e-9

def test_dataset_real_gerado_classifica_corretamente():
    ref = pd.read_csv("data/referencia.csv")
    ok = pd.read_csv("data/producao_estavel.csv")
    drift = pd.read_csv("data/producao_drift.csv")
    r_ok = analisar_dataset(ref, ok)
    r_dr = analisar_dataset(ref, drift)
    assert r_ok["status"] == "ESTAVEL"
    assert r_ok["colunas_com_drift"] <= 1
    assert r_dr["status"] == "ALERTA"
    assert r_dr["colunas_com_drift"] >= 3

def test_resultados_tem_todas_colunas():
    ref = pd.read_csv("data/referencia.csv")
    drift = pd.read_csv("data/producao_drift.csv")
    r = analisar_dataset(ref, drift)
    nomes = {x["coluna"] for x in r["resultados"]}
    assert nomes == {"idade","meses_cliente","chamados_suporte","dias_sem_login","valor_mensal","canal"}
