
# Dockerfile
# Imagem de inferência: contém API FastAPI, dependências e modelo treinado.

# Usa imagem Python enxuta para reduzir tamanho final.
FROM python:3.11-slim

# Impede Python de criar arquivos .pyc dentro do container.
ENV PYTHONDONTWRITEBYTECODE=1

# Faz logs aparecerem imediatamente no terminal do Docker.
ENV PYTHONUNBUFFERED=1

# Define a pasta de trabalho dentro do container.
WORKDIR /app

# Copia primeiro as dependências para aproveitar cache de build.
COPY requirements.txt .

# Instala dependências sem guardar cache do pip.
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da API para dentro da imagem.
COPY src/ ./src/

# Copia o modelo treinado para dentro da imagem.
COPY models/ ./models/

# Cria usuário sem privilégios de root.
RUN useradd --create-home --shell /bin/bash appuser

# Executa o servidor como usuário não-root.
USER appuser

# Documenta que a aplicação escuta na porta 8000.
EXPOSE 8000

# Inicia o servidor FastAPI com uvicorn.
CMD ["uvicorn", "src.serve:app", "--host", "0.0.0.0", "--port", "8000"]
