# pull official base image
FROM python:3.11.2-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
# lint
RUN pip install flake8
COPY . .
#RUN flake8 --exclude venv,migration --ignore=E501,F401,F841,E128

COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
