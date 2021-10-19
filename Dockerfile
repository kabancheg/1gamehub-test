FROM python:3.6
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /var/opt/app
WORKDIR /var/opt/app
COPY . /var/opt/app
COPY ./init.sql /docker-entrypoint-initdb.d/
RUN python -m pip install --upgrade pip
RUN pip install -r ./app/requirements.txt

ENV DJANGO_ENV=prod
ENV DOCKER_CONTAINER=1

EXPOSE 8000