
# 1. Criar o modelo local
python scripts/create_model.py

# 2. Build da imagem
docker build -t modelo-inferencia:1.0 .

# 3. Rodar o container
docker run -p 8000:8000 --rm modelo-inferencia:1.0

# 4. Em outro terminal, testar health check
curl http://localhost:8000/

# 5. Em outro terminal, testar predição
curl -X POST http://localhost:8000/predict `
  -H "Content-Type: application/json" `
  -d "{\"features\":[0.5,-1.2,0.8,1.1,-0.3,0.6,1.5,-0.9,0.2,0.7]}"

# 6. Ver tamanho da imagem
docker images modelo-inferencia

# 7. Testar compose
docker compose up --build
