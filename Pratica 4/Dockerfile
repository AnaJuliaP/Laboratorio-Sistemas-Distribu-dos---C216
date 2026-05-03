# Imagem base Python slim
FROM python:3.10-slim

# Diretório de trabalho
WORKDIR /app

# Instala dependências primeiro (cache de layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY . .

# Expõe a porta da API
EXPOSE 8000

# Sobe a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]