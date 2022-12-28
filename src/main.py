import logs
import os
from core.beans_bot import beans_bot
from discord import Intents

if __name__ == '__main__':
    token = os.getenv('TOKEN')

    logs.logger.info('Beans Bot Starting...')

    intents = Intents.default()
    intents.message_content = True
    intents.members = True

    bot = beans_bot(token, intents)
    bot.start()
