import discord, os, alexisms, doingMaths, logs
from dotenv import load_dotenv
import random as rand

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
   logs.logger.info("{0.user} is now online".format(client))

@client.event
async def on_message(message):

    # check to see if the user is mentioned
    if client.user.mentioned_in(message):
        await message.channel.send("The fuck do you want you lairy bastard")

    # to prevent the bot from triggering itself if it finds a response in 
    if message.author == client.user:
        return

    # in a message someone might say multiple trigger words: e.g. Alex and shit 
    # identify all trigger words that exist in a message 
    trigger_words = [key for key in alexisms.phrases.keys() if key in message.content.lower()]  

    for trigger_word in trigger_words: 
        responses = alexisms.phrases[trigger_word]
        if isinstance(responses, list):
            await message.channel.send(rand.choice(responses)) 

        elif isinstance(responses, str):
            await message.channel.send(responses) 

        else:
            return

    # maths
    if doingMaths.isEquation(message.content) == True:
        logs.logger.info("{0.user} is doing maths".format(client))
        await message.channel.send("I'm doing maaaaaaaaaaths")
        await message.channel.send(doingMaths.doMaths(message.content))

load_dotenv()
token = os.getenv('TOKEN')
client.run(token)