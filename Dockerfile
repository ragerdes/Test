FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv/latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_INSTALL_DIR=/opt/python \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src
COPY worker.py ./

RUN uv sync --no-dev

CMD ["python", "worker.py"]
