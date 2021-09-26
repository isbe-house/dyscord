FROM python:3 as PROD

WORKDIR /usr/src/app

RUN apt update
RUN apt install -y vim

COPY requirements.txt ./
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir pytest pytest-cov flake8
RUN pip install --no-cache-dir -r requirements.txt

FROM PROD as TEST

COPY requirements_test.txt ./
RUN pip install --no-cache-dir -r requirements_test.txt
# Handle testing modules, not needed for deployment

