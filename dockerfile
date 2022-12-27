FROM python:latest
LABEL Maintainer='Tetracionist'

WORKDIR /discord-bots/beans-bot

COPY src/ .

RUN adduser -u 5678 --disabled-password --gecos "" botuser && chown -R botuser /discord-bots/beans-bot
USER botuser

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

CMD ["python", "main.py"]
