from core.beansBot import beansBot
from discord import Intents
from core import logs, alexisms
from dotenv import load_dotenv
import os, random


if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TOKEN')

    intents = Intents.default()
    intents.message_content = True

    bot = beansBot(token, intents)
    bot.start()
