
########################################################################################################################

 # BASE IMAGE
########################################################################################################################

# pull offical base image
FROM python:3.7-alpine as base

#No cache files and buffering
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Required by alpine to run uWSGI
RUN apk add --update --no-cache libc-dev \
   linux-headers \
   build-base \
  cairo \
  cairo-dev \
  cargo \
  freetype-dev \
  gcc \
  gdk-pixbuf-dev \
  gettext \
  jpeg-dev \
  lcms2-dev \
  libffi-dev \
  musl-dev \
  openjpeg-dev \
  openssl-dev \
  pango-dev \
  poppler-utils \
  py-cffi \
  python3-dev \
  rust \
  tcl-dev \
  tiff-dev \
  tk-dev \
  zlib-dev \
  libxslt-dev \
   libxml2-dev \
   openssl-dev \
   mariadb-connector-c-dev

########################################################################################################################

 # BUILD IMAGE
########################################################################################################################
FROM base as builder


ENV  POETRY_VERSION=1.1.5 \
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1

# pip and python basic configurations

ENV PATH=/venv/bin:$PATH

RUN python -m venv /venv

COPY pyproject.toml .

RUN pip install --upgrade pip  && pip --no-cache-dir install "poetry==$POETRY_VERSION"

RUN poetry export --without-hashes --format requirements.txt --output requirements.txt

RUN pip install -r requirements.txt



########################################################################################################################

 # DEPLOY
########################################################################################################################
FROM base as final

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PATH=/venv/bin:$PATH


COPY --from=builder /venv /venv

RUN mkdir /app
COPY . /app
WORKDIR /app
RUN mkdir /scripts
COPY ./scripts /scripts
RUN chmod +x /scripts/*

# Create folders for the media being served

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN mkdir -p /vol/web/whoosh_index

# Create new user in the application, no root
RUN adduser -D user
#User can access the vol
RUN chown -R user:user /vol

#full access
RUN chmod -R 755 /vol/web

USER user

EXPOSE 8000

CMD [".docker-entrypoint.sh"]

