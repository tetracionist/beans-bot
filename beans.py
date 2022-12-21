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
async def on_voice_state_update(member, before, after):
   
    #print(f"member: {member}, before.channel:{before.channel}, after.channel: {after.channel}, before.id: {member.id}")

    

    # check that the id is not beans bot
    if member.id == 1054876494222078012:
        return

    audio_source = discord.FFmpegPCMAudio('beans.mp3')

    # check for existing connection 
    if not client.voice_clients and after.channel != None:
        # create a voice client by connecting to user's channel
        channel = await client.fetch_channel(after.channel.id)
        await channel.connect()
        voice_client = discord.utils.get(client.voice_clients)
        logs.logger.info("{0.user} created a new voice client".format(client))
        voice_client.play(audio_source, after=None)

    else:
        # check if user has switched channels
        if before.channel != after.channel and after.channel:
            # find the voice client that is connected to the channel the user has switched to
            next_channel = await client.fetch_channel(after.channel.id)
            for vc in client.voice_clients:
                if vc.channel == next_channel:
                    voice_client = vc
                    break
            else:
                # if no voice client was found, use the first voice client in the list
                voice_client = client.voice_clients[0]

            logs.logger.info(f"channel switch on {voice_client}")
            # move the voice client to the new channel
            await voice_client.move_to(next_channel)

            # play the audio file
            if voice_client.is_playing():
                voice_client.stop()
            voice_client.play(audio_source, after=None)
        
        elif after.channel == None:
            previous_channel = await client.fetch_channel(before.channel.id)
            for vc in client.voice_clients:
                if vc.channel == previous_channel:
                    voice_client = vc
                    break
            else:
                # if no voice client was found, use the first voice client in the list
                voice_client = client.voice_clients[0]
            await voice_client.disconnect()

    # Clean up the audio source after it has finished playing
    #audio_source.cleanup()


    

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