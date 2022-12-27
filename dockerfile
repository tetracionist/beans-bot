FROM python:latest
LABEL Maintainer='Tetracionist'

WORKDIR /discord-bots/beans-bot

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY src/ .

RUN adduser -u 5678 --disabled-password --gecos "" botuser && chown -R botuser /discord-bots/beans-bot
USER botuser

CMD ["python", "main.py"]
