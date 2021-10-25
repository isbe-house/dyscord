FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN pip install --upgrade twine build setuptools

COPY tests/requirements_test.txt ./
RUN pip install -r requirements_test.txt