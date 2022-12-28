from core.beansBot import beansBot
from core.commands import Command
from discord import Intents
from core import alexisms
import os, random, re, logs
from dotenv import load_dotenv

if __name__ == '__main__':
    
    logs.logger.info('Beans Bot Starting...')

    load_dotenv()
    token = os.getenv('TOKEN')

    intents = Intents.default()
    intents.message_content = True
    intents.members = True

    bot = beansBot(token, intents)
    bot.start()
