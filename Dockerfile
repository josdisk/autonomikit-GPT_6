FROM python:3.11-slim

WORKDIR /app
ENV PIP_NO_CACHE_DIR=1

COPY pyproject.toml README.md /app/
COPY src /app/src
COPY .env.example /app/.env.example

RUN pip install -U pip && pip install -e .

EXPOSE 8000
CMD ["autonomi", "api"]
