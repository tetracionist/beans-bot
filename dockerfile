FROM python:latest
LABEL Maintainer='Tetracionist'

WORKDIR /discord-bots/beans-bot

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN adduser -u 5678 --disabled-password --gecos "" botuser && chown -R botuser /discord-bots/beans-bot
USER botuser

CMD ["python", "beans.py"]