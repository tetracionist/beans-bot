from core.beansBot import beansBot
from core.commands import Command
from discord import Intents
from core import logs, alexisms
import os, random, re


if __name__ == '__main__':
    token = os.getenv('TOKEN')

    intents = Intents.default()
    intents.message_content = True
    intents.members = True

    bot = beansBot(token, intents)
    bot.start()
