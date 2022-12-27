FROM python:latest
LABEL Maintainer='Tetracionist'

WORKDIR /discord-bots/beans-bot

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

RUN python -m venv /opt/venv

COPY requirements.txt requirements.txt
RUN /opt/venv/bin/pip install -r requirements.txt


COPY src/ .

RUN adduser -u 5678 --disabled-password --gecos "" botuser && chown -R botuser /discord-bots/beans-bot
USER botuser

CMD ["python", "main.py"]
