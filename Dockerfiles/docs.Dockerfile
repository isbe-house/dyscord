FROM python:3.9

COPY requirements.txt ./
COPY docs/requirements_docs.txt ./docs/
RUN pip install -r ./docs/requirements_docs.txt
WORKDIR /usr/src/app
