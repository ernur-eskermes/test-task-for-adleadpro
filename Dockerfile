FROM python:3.9 as builder

WORKDIR /usr/src/polls_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get upgrade -y && apt-get install postgresql gcc python3-dev musl-dev vim -y

RUN pip install --upgrade pip

COPY . /usr/src/polls_app

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/polls_app/wheels -r requirements.txt

FROM python:3.9

RUN mkdir -p /home/app

ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN apt-get update \
    && apt-get install -y netcat

COPY --from=builder /usr/src/polls_app/wheels /wheels
COPY --from=builder /usr/src/polls_app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY . $APP_HOME
