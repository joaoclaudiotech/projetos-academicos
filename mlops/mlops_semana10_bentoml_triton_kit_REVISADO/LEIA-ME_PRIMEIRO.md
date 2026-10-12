# MLOps · Semana 10 — BentoML e Triton

Este kit foi preparado para Windows + Visual Studio Code + PowerShell.

## Objetivo
Transformar um modelo de churn em um serviço BentoML atual, registrar o modelo no Model Store, testar a API, comparar uma API FastAPI simples com o BentoML e observar o efeito de batching/adaptive batching.

## Ordem obrigatória
1. Abra ESTA pasta no VS Code (`Arquivo > Abrir Pasta`).
2. Abra `Terminal > Novo Terminal` e confirme que o terminal é PowerShell.
3. Crie e ative a venv:
   - `py -m venv .venv`
   - `.\.venv\Scripts\Activate.ps1`
4. Instale: `python -m pip install -r requirements.txt`
5. Rode: `python 00_preflight.py`
6. Treine: `python 01_treinar_modelo.py`
7. Registre: `python 02_registrar_bentoml.py`
8. Sirva: `bentoml serve service:ChurnService --reload`
9. Abra `http://localhost:3000`.
10. Em OUTRO terminal ativado, rode: `python 03_validar_servico.py`
11. Para comparação com FastAPI, siga o caderno do aluno.

## Importante
- Não digite comandos no terminal onde o servidor BentoML está rodando. Abra outro terminal.
- Se a ativação da venv for bloqueada no PowerShell, use apenas nesta janela:
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
- O Docker é OPCIONAL nesta aula. A prática principal não depende dele.
- BentoML 1.4.39 usa o modelo moderno de Service baseado em classe (`@bentoml.service` / `@bentoml.api`).
