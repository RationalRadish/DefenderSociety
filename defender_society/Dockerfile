
########################################################################################################################

 # BASE IMAGE
########################################################################################################################

# pull offical base image
FROM python:3.7-alpine as base

#No cache files and buffering
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.1.5 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"


# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"



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

# pip and python basic configurations

RUN python -m venv /venv

WORKDIR $PYSETUP_PATH

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip  && pip --no-cache-dir install "poetry==$POETRY_VERSION"

RUN poetry install --no-root --no-dev




########################################################################################################################

 # DEPLOY
########################################################################################################################
FROM base as poetry_build

WORKDIR $PYSETUP_PATH

COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

RUN poetry install --no-root --no-dev



# Add scripts to the containers path. Can access them just by running.

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
#RUN adduser -D user
#User can access the vol
#RUN chown -R user:user /vol

#full access
RUN chmod -R 755 /vol/web

RUN . /venv/bin/activate

#USER user

CMD [".docker-entrypoint.sh"]

