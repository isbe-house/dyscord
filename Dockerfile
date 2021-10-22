FROM python:3.9 as PROD

WORKDIR /usr/src/app

RUN apt update
RUN apt install -y vim

COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

FROM PROD as TEST

# We want to detect out of date build envs too!
RUN pip install --no-cache-dir --upgrade twine build setuptools

COPY requirements_test.txt ./
RUN pip install --no-cache-dir -r requirements_test.txt
# Handle testing modules, not needed for deployment

FROM python:3.9 as DOCS

COPY requirements.txt ./
COPY requirements_docs.txt ./
RUN pip install --no-cache-dir -r requirements_docs.txt
ENV PYTHONPATH=src
WORKDIR /usr/src/app

FROM python:3.9 as RELEASE

WORKDIR /usr/src/app

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade twine build setuptools

ARG TWINE_USERNAME
ARG TWINE_PASSWORD