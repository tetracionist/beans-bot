import logs
import os
from core.beans_bot import beans_bot
from discord import Intents
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    token = os.getenv('TOKEN')

    logs.logger.info('Beans Bot Starting...')

    intents = Intents.default()
    intents.message_content = True
    intents.members = True

    bot = beans_bot(token, intents)
    bot.start()
