FROM python:3.9 as PROD

WORKDIR /usr/src/app

RUN apt update
RUN apt install -y vim

COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

FROM PROD as TEST

COPY requirements_test.txt ./
RUN pip install --no-cache-dir -r requirements_test.txt
# Handle testing modules, not needed for deployment

FROM TEST as DOCS

RUN pip install --no-cache-dir mkdocs mkdocstrings mkdocs-autorefs mkdocs-material
ENV PYTHONPATH=src

FROM python:3.9 as RELEASE

WORKDIR /usr/src/app

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir twine

ARG TWINE_USERNAME
ARG TWINE_PASSWORD