FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . .

RUN chmod +x entrypoint.sh

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

RUN pip install --no-cache-dir --use-deprecated=legacy-resolver "psutil==5.9.8"

RUN poetry config installer.max-workers 10

RUN poetry install --no-interaction --no-ansi

EXPOSE 8000

CMD poetry run fastapi run fast_zero/app.py