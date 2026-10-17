from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

Path("reports").mkdir(exist_ok=True)
ref = pd.read_csv("data/referencia.csv")
ok = pd.read_csv("data/producao_estavel.csv")
drift = pd.read_csv("data/producao_drift.csv")

for coluna in ["dias_sem_login", "valor_mensal"]:
    plt.figure(figsize=(8, 4.5))
    plt.hist(ref[coluna], bins=28, alpha=0.45, density=True, label="Referência")
    plt.hist(ok[coluna], bins=28, alpha=0.45, density=True, label="Produção estável")
    plt.hist(drift[coluna], bins=28, alpha=0.45, density=True, label="Produção com drift")
    plt.xlabel(coluna)
    plt.ylabel("densidade")
    plt.title(f"Comparação de distribuição — {coluna}")
    plt.legend()
    plt.tight_layout()
    path = Path("reports") / f"distribuicao_{coluna}.png"
    plt.savefig(path, dpi=150)
    plt.close()
    print("[OK]", path)
