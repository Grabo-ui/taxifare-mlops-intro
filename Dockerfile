FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src src

RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev

COPY api api

CMD uv run uvicorn api.fast:app --host 0.0.0.0 --port $PORT
