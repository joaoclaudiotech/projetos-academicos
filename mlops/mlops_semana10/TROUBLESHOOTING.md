# Troubleshooting — Semana 10

## 1. `bentoml` não é reconhecido
Confirme que a venv está ativada. No Windows/PowerShell, verifique:
`Get-Command bentoml`

Se o comando não aparecer, chame o executável da própria venv diretamente, por exemplo:
`& .\.venv\Scripts\bentoml.exe --version`

## 2. `ModuleNotFoundError: bentoml`
`python -m pip install -r requirements.txt`

## 3. PowerShell bloqueia `.ps1`
Somente no terminal atual:
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
Depois: `.\.venv\Scripts\Activate.ps1`

## 4. `classificador_churn:latest` não encontrado
Rode, nesta ordem:
`python 01_treinar_modelo.py`
`python 02_registrar_bentoml.py`

## 5. Porta 3000 ocupada
Feche outro BentoML ou use outra porta:
`bentoml serve service:ChurnService --port 3001`
Se mudar a porta, ajuste os scripts de validação/benchmark ou volte para 3000.

## 6. Porta 8000 ocupada
Feche a API antiga ou use o Gerenciador de Tarefas. A prática foi documentada assumindo 8000.

## 7. Não consigo digitar comandos
Você provavelmente está no terminal do servidor. Ele precisa continuar rodando. Abra `Terminal > Novo Terminal`.

## 8. Docker não funciona
Docker é trilha opcional. NÃO interrompa a atividade principal. Continue até o build do Bento e registre a limitação na reflexão.

## 9. Benchmark deu números diferentes do colega
Esperado. CPU, processos abertos, antivírus, aquecimento, versões e concorrência alteram os resultados. Compare tendências e métricas, não um número “certo”.
