# MLOps — Semana 09 — FastAPI para Serving de Modelos

Este kit foi preparado para **Windows + Visual Studio Code + PowerShell** e é autossuficiente:
você não precisa recuperar um `model.pkl` de outra semana.

## Estrutura

```text
mlops_semana09_fastapi_kit_pratica/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  └─ model.py
├─ scripts/
│  ├─ train_model.py
│  └─ validar_entrega.py
├─ models/
├─ exemplos/
│  └─ payloads.json
├─ requirements.txt
├─ COMECE_AQUI.txt
└─ LEIA-ME.md
```

## Rota recomendada no Windows

Abra a pasta inteira no VS Code. Depois use **Terminal > New Terminal**.

### 1) Criar ambiente virtual

```powershell
py -m venv .venv
```

Se `py` não existir:

```powershell
python -m venv .venv
```

### 2) Ativar no PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

Se aparecer bloqueio de execução de scripts, use apenas neste terminal:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Alternativa pelo Prompt de Comando (CMD):

```bat
.venv\Scripts\activate.bat
```

### 3) Instalar

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4) Treinar e gerar o modelo

```powershell
python scripts\train_model.py
```

Deve aparecer `OK - modelo treinado` e ser criado `models\model.json`.

### 5) Terminal 1 — manter a API ligada

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

Não feche este terminal durante os testes.

Abra no navegador:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

### 6) Terminal 2 — validação automática

No VS Code clique no botão `+` do painel Terminal para abrir outro terminal.
Ative o ambiente novamente se necessário:

```powershell
.\.venv\Scripts\Activate.ps1
python scripts\validar_entrega.py
```

Esperado: `7/7 verificações passaram`.

## Por que não usamos `curl` como primeiro teste?

No Windows/PowerShell, `curl` pode ser interpretado de maneiras diferentes conforme a versão/configuração.
O caminho principal desta aula é **Swagger UI** e o script Python de validação. Assim o foco fica
em FastAPI/Pydantic e não em diferenças de shell.

## Parar a API

Volte ao Terminal 1 e pressione `Ctrl + C`.
