FROM python
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code
ENV PATH=/code/.venv/bin:$PATH

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-install-project

COPY ingest_data.py .

ENTRYPOINT ["python", "ingest_data.py"]