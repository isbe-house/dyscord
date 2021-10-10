FROM jupyter/scipy-notebook:b94c2f2db600

USER root

RUN apt update
RUN apt install -y vim

COPY requirements_test.txt ./
RUN pip install --no-cache-dir -r requirements_test.txt
RUN rm requirements_test.txt

COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt
