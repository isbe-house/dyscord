FROM python:3.9 as RELEASE

WORKDIR /usr/src/app

RUN python -m pip install --upgrade pip
RUN pip install --upgrade twine build setuptools

ARG TWINE_USERNAME
ARG TWINE_PASSWORD