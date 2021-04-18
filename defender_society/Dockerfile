
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
   mariadb-connector-c-dev \
   postgresql \
   postgresql-dev

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


RUN pip install --upgrade pip  && pip install wheel && pip --no-cache-dir install "poetry==$POETRY_VERSION"

RUN poetry export --without-hashes --format requirements.txt --output requirements.txt

RUN pip install -r requirements.txt && pip install gunicorn && pip install psycopg2-binary



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
COPY  prod-entrypoint.sh  /prod-entrypoint.sh
RUN chmod +x /prod-entrypoint.sh

# Create folders for the media being served

RUN mkdir -p /vol/media && mkdir -p /vol/static && mkdir -p /vol/whoosh_index

# Create new user in the application, no root. #User can access the vol

#RUN adduser -D user

#RUN chown -R user:user /vol

#RUN chmod -R 755 /vol/web



EXPOSE 8000


#USER user


#CMD ["uwsgi", "--ini", "uwsgi.ini"]
CMD [ "/prod-entrypoint.sh"]
