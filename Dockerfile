FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copia o restante do código (app/, alembic/, etc.)
COPY . .

EXPOSE 8000

# O --host 0.0.0.0 é obrigatório para aceitar conexões de fora do container
CMD ["uvicorn", "main:APP", "--host", "0.0.0.0", "--port", "8000"]