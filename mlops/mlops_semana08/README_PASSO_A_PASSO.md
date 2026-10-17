
# MLOps Semana 8 — Docker para inferência de ML

Este projeto gera um modelo simples, cria uma API FastAPI e empacota tudo em Docker.

## Ordem correta

```bash
pip install -r requirements.txt
python scripts/create_model.py
docker build -t modelo-inferencia:1.0 .
docker run -p 8000:8000 --rm modelo-inferencia:1.0
```

Em outro terminal:

```bash
curl http://localhost:8000/

curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features":[0.5,-1.2,0.8,1.1,-0.3,0.6,1.5,-0.9,0.2,0.7]}'
```

## Evidências esperadas

- `models/model.pkl` criado.
- `docker build` finalizado sem erro.
- `docker run` mostrando Uvicorn em `0.0.0.0:8000`.
- `curl /` retornando `{"status":"ok", ...}`.
- `curl /predict` retornando `prediction` e `probability`.

## Arquivos principais

- `scripts/create_model.py`: cria modelo didático.
- `src/serve.py`: API FastAPI de inferência.
- `Dockerfile`: imagem de inferência enxuta.
- `.dockerignore`: evita mandar dados/secrets para a imagem.
- `docker-compose.yml`: sobe o serviço com um comando.
