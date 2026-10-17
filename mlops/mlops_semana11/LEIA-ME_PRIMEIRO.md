# Semana 11 — Monitoramento em Produção e Data Drift

## Objetivo
Comparar uma **referência** (perfil conhecido) com novos lotes de produção, detectar mudanças de distribuição, gerar evidências visuais e automatizar uma decisão operacional de monitoramento.

## Ambiente recomendado
- Windows 10/11
- VS Code
- Python 3.10+
- Internet apenas para a primeira instalação das dependências

## Início no PowerShell
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python 00_preflight.py
```
Se o PowerShell bloquear a ativação:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Sequência da prática
```powershell
python 01_gerar_dados.py
python 02_visualizar_distribuicoes.py
python 03_analisar_drift_manual.py
python 04_relatorios_evidently.py
python 05_pipeline_monitor.py --dataset estavel
python 05_pipeline_monitor.py --dataset drift
python 06_validar_entrega.py
```

## Importante sobre Evidently
Este kit usa a API atual da linha 0.7.x:
```python
from evidently import Report
from evidently.presets import DataDriftPreset
```
Não use exemplos antigos com `from evidently.report import Report`, `evidently.metric_preset` ou `TestSuite` separado.

## Entrega
Abra `CADERNO_ALUNO_SEMANA11.html`, preencha nome/turma, anexe as evidências solicitadas, responda às questões e use **Imprimir / Salvar PDF**. Guarde também o JSON de progresso.
