ARG PYTHON_VERSION=3.10.10

FROM python:${PYTHON_VERSION}-slim

ARG ENV
ARG POETRY_VERSION=1.3.2

ENV ENV=${ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=${POETRY_VERSION} \
  POETRY_HOME=/usr/local

# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    wget \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
  && pip install "poetry==$POETRY_VERSION" && poetry --version

# set work directory
WORKDIR /home/app

# Install dependencies:
RUN poetry config --local virtualenvs.create true \
    && poetry config --local virtualenvs.in-project true

# copy project
COPY src ./src
COPY ./scripts ./
COPY pyproject.toml poetry.lock README.md /home/app/

RUN poetry install
RUN mkdir /home/app/video_data

ENTRYPOINT [ "./entrypoint.sh" ]

