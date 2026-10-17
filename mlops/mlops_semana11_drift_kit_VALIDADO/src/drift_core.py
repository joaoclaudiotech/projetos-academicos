from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json
import math
import numpy as np
import pandas as pd
from scipy import stats

NUMERICAS = ["idade", "meses_cliente", "chamados_suporte", "dias_sem_login", "valor_mensal"]
CATEGORICAS = ["canal"]

@dataclass
class ResultadoColuna:
    coluna: str
    tipo: str
    metodo: str
    estatistica: float
    p_value: float | None
    psi: float | None
    drift: bool
    criterio: str


def _safe_freq(counts: np.ndarray) -> np.ndarray:
    counts = counts.astype(float)
    total = counts.sum()
    if total == 0:
        return np.full_like(counts, 1.0 / len(counts), dtype=float)
    f = counts / total
    eps = 1e-6
    f = np.clip(f, eps, None)
    return f / f.sum()


def psi_numerico(referencia: pd.Series, atual: pd.Series, bins: int = 10) -> float:
    ref = pd.to_numeric(referencia, errors="coerce").dropna().to_numpy(float)
    cur = pd.to_numeric(atual, errors="coerce").dropna().to_numpy(float)
    if len(ref) < 2 or len(cur) < 2:
        return float("nan")
    edges = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    if len(edges) < 3:
        lo = min(ref.min(), cur.min())
        hi = max(ref.max(), cur.max())
        if math.isclose(lo, hi):
            return 0.0
        edges = np.linspace(lo, hi, bins + 1)
    edges[0] = -np.inf
    edges[-1] = np.inf
    ref_f = _safe_freq(np.histogram(ref, bins=edges)[0])
    cur_f = _safe_freq(np.histogram(cur, bins=edges)[0])
    return float(np.sum((cur_f - ref_f) * np.log(cur_f / ref_f)))


def chi_quadrado_categorico(referencia: pd.Series, atual: pd.Series) -> tuple[float, float]:
    ref = referencia.fillna("<NULO>").astype(str)
    cur = atual.fillna("<NULO>").astype(str)
    cats = sorted(set(ref.unique()) | set(cur.unique()))
    ref_counts = np.array([(ref == c).sum() for c in cats], dtype=float)
    cur_counts = np.array([(cur == c).sum() for c in cats], dtype=float)
    ref_prop = _safe_freq(ref_counts)
    expected = ref_prop * cur_counts.sum()
    expected = np.clip(expected, 1e-6, None)
    stat = float(np.sum((cur_counts - expected) ** 2 / expected))
    df = max(1, len(cats) - 1)
    p = float(stats.chi2.sf(stat, df))
    return stat, p


def analisar_coluna_numerica(ref: pd.Series, cur: pd.Series, nome: str) -> ResultadoColuna:
    ks_stat, ks_p = stats.ks_2samp(ref.dropna(), cur.dropna(), alternative="two-sided", method="auto")
    psi = psi_numerico(ref, cur)
    # Dupla evidencia reduz falso alarme didatico: significancia + magnitude.
    drift = bool(ks_p < 0.01 and psi >= 0.20)
    return ResultadoColuna(
        coluna=nome,
        tipo="numerica",
        metodo="KS + PSI",
        estatistica=float(ks_stat),
        p_value=float(ks_p),
        psi=float(psi),
        drift=drift,
        criterio="drift se p(KS)<0,01 E PSI>=0,20",
    )


def analisar_coluna_categorica(ref: pd.Series, cur: pd.Series, nome: str) -> ResultadoColuna:
    stat, p = chi_quadrado_categorico(ref, cur)
    return ResultadoColuna(
        coluna=nome,
        tipo="categorica",
        metodo="Qui-quadrado",
        estatistica=stat,
        p_value=p,
        psi=None,
        drift=bool(p < 0.01),
        criterio="drift se p(qui-quadrado)<0,01",
    )


def analisar_dataset(referencia: pd.DataFrame, atual: pd.DataFrame) -> dict:
    faltantes = [c for c in NUMERICAS + CATEGORICAS if c not in referencia.columns or c not in atual.columns]
    if faltantes:
        raise ValueError(f"Colunas ausentes: {faltantes}")
    resultados: list[ResultadoColuna] = []
    for c in NUMERICAS:
        resultados.append(analisar_coluna_numerica(referencia[c], atual[c], c))
    for c in CATEGORICAS:
        resultados.append(analisar_coluna_categorica(referencia[c], atual[c], c))
    n = len(resultados)
    n_drift = sum(r.drift for r in resultados)
    share = n_drift / n if n else 0.0
    # Regra operacional didatica: alerta quando >= 2 colunas ou >= 30%.
    alerta = bool(n_drift >= 2 or share >= 0.30)
    return {
        "total_colunas": n,
        "colunas_com_drift": n_drift,
        "share_drift": round(share, 4),
        "status": "ALERTA" if alerta else "ESTAVEL",
        "regra_operacional": "ALERTA se >=2 colunas com drift OU share>=30%",
        "resultados": [asdict(r) for r in resultados],
    }


def salvar_json(obj: dict, caminho: str | Path) -> None:
    p = Path(caminho)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def resumo_html(nome: str, resumo: dict) -> str:
    rows = []
    for r in resumo["resultados"]:
        cls = "bad" if r["drift"] else "ok"
        psi = "—" if r["psi"] is None else f'{r["psi"]:.3f}'
        p = "—" if r["p_value"] is None else f'{r["p_value"]:.3g}'
        rows.append(f"<tr><td>{r['coluna']}</td><td>{r['metodo']}</td><td>{r['estatistica']:.3f}</td><td>{p}</td><td>{psi}</td><td class='{cls}'>{'DRIFT' if r['drift'] else 'OK'}</td></tr>")
    status_cls = "bad" if resumo["status"] == "ALERTA" else "ok"
    return f"""<!doctype html><html lang='pt-BR'><meta charset='utf-8'><title>Drift - {nome}</title>
<style>body{{font-family:Arial,sans-serif;max-width:1050px;margin:40px auto;padding:0 20px;background:#111827;color:#e5e7eb}}h1{{margin-bottom:5px}}.card{{background:#1f2937;border:1px solid #374151;border-radius:14px;padding:18px;margin:18px 0}}table{{width:100%;border-collapse:collapse}}td,th{{padding:10px;border-bottom:1px solid #374151;text-align:left}}.ok{{color:#4ade80;font-weight:700}}.bad{{color:#f87171;font-weight:700}}small{{color:#9ca3af}}</style>
<h1>Monitoramento de drift — {nome}</h1><p class='{status_cls}'>Status operacional: {resumo['status']}</p>
<div class='card'><b>{resumo['colunas_com_drift']}</b> de {resumo['total_colunas']} colunas com drift · share={resumo['share_drift']:.0%}<br><small>{resumo['regra_operacional']}</small></div>
<div class='card'><table><thead><tr><th>Coluna</th><th>Método</th><th>Estatística</th><th>p-value</th><th>PSI</th><th>Decisão</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<p><small>Material didático: os limiares são critérios operacionais definidos para a prática, não leis universais.</small></p></html>"""
