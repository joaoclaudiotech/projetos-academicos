from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path("data")
OUT.mkdir(exist_ok=True)

def base(seed: int, n: int) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    idade = np.clip(rng.normal(38, 10, n), 18, 80).round().astype(int)
    meses = np.clip(rng.gamma(2.6, 11.0, n), 0, 180).round().astype(int)
    chamados = np.clip(rng.poisson(2.0, n), 0, 20).astype(int)
    dias = np.clip(rng.exponential(12.0, n), 0, 180).round().astype(int)
    valor = np.clip(rng.normal(150, 35, n), 40, 450).round(2)
    canal = rng.choice(["app", "web", "loja"], n, p=[0.45, 0.40, 0.15])
    return pd.DataFrame({
        "idade": idade,
        "meses_cliente": meses,
        "chamados_suporte": chamados,
        "dias_sem_login": dias,
        "valor_mensal": valor,
        "canal": canal,
    })

ref = base(42, 1200)
ok = base(123, 600)
drift = base(321, 600)
rng = np.random.default_rng(999)
# Mudanças intencionais de produção: suporte, inatividade, valor e canal.
drift["chamados_suporte"] = np.clip(rng.poisson(5.2, len(drift)), 0, 25)
drift["dias_sem_login"] = np.clip(rng.exponential(32.0, len(drift)), 0, 240).round().astype(int)
drift["valor_mensal"] = np.clip(rng.normal(215, 42, len(drift)), 40, 500).round(2)
drift["canal"] = rng.choice(["app", "web", "loja"], len(drift), p=[0.70, 0.20, 0.10])

for nome, df in [("referencia", ref), ("producao_estavel", ok), ("producao_drift", drift)]:
    path = OUT / f"{nome}.csv"
    df.to_csv(path, index=False)
    print(f"[OK] {path} -> {len(df)} linhas")
print("\nDados gerados. A referência representa o perfil conhecido; os dois lotes simulam produção.")
