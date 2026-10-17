# Troubleshooting — Semana 11

## `python` não encontrado
Instale Python 3.10+ e marque **Add Python to PATH**. Depois feche e abra o VS Code.

## PowerShell não deixa ativar `.venv`
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## `ModuleNotFoundError`
Confirme se o terminal mostra `(.venv)` e execute:
```powershell
python -m pip install -r requirements.txt
python 00_preflight.py
```

## Evidently não instala
1. Confirme internet.
2. Rode `python -m pip install --upgrade pip`.
3. Rode novamente `python -m pip install -r requirements.txt`.
4. Não troque a versão sem autorização: o caderno foi escrito para `evidently==0.7.23`.

## Relatórios Evidently não aparecem
Execute primeiro `01_gerar_dados.py` e depois `04_relatorios_evidently.py`. Verifique a pasta `reports/`.

## Validador mostra FAIL somente nos dois relatórios Evidently
Isso significa que as etapas manuais funcionaram, mas a etapa 04 ainda não foi concluída. Corrija a instalação do Evidently e execute novamente.

## O resultado do drift é diferente em outra turma/máquina
Os dados do kit usam sementes fixas. Se os CSVs foram alterados, regenere com `python 01_gerar_dados.py`.
