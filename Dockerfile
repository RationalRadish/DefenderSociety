# pull offical base image
FROM python:3.7-slim as base

#No cache files and buffering
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y gcc libffi-dev g++

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT = 100\
    PIP_DISABLE_PIP_VERSION_CHECK=1\
    PIP_NO_CACHE_DIR=1\
    POETRY_VERSION = 1.1.3

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./

RUN . /venv/bin/activate && poetry install --no-root $(test "$YOUR_ENV" == production && echo "--no-dev")

COPY . .
RUN . /venv/bin/activate && poetry build


FROM base as final

COPY --from=builder /venv /venv
COPY --from=builder /app/dist
COPY docker-entrypoint.sh ./

RUN . /venv/bin/activate && pip install *.whl
CMD [".docker-entrypoint.sh"]

