import discord, os, alexisms
from dotenv import load_dotenv
import random as rand



intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)



@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):

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




load_dotenv()
token = os.getenv('TOKEN')
client.run(token)