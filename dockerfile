FROM python:latest
LABEL Maintainer='Tetracionist'

WORKDIR /discord-bots/beans-bot

RUN python -m venv /opt/venv

COPY requirements.txt requirements.txt
RUN /opt/venv/bin/pip install -r requirements.txt
RUN apt-get install ffmpeg

COPY . .

RUN adduser -u 5678 --disabled-password --gecos "" botuser && chown -R botuser /discord-bots/beans-bot
USER botuser

CMD ["python", "beans.py"]