import discord
import random as rand
import core.alexisms
import core.voice
import core.commands
import logs
import os
import asyncio


class beans_bot:
    def __init__(self: object, token: str, intents: object, prefix='!bb'):
        self.token = token
        self.intents = intents
        self.client = discord.Client(intents=intents)
        self.prefix = prefix
        self.target_dict = {}

        # define commands
        self.commands = {"ping": core.commands.ping_command(self),
                         "target": core.commands.target_command(self),
                         "speak": core.commands.speak_command(self),
                         "say": core.commands.say_command(self),
                         "do_maths": core.commands.do_maths_command(self)}

    def start(self):
        @self.client.event
        async def on_ready():
            logs.logger.info('Log In Successful')

        @self.client.event
        async def on_voice_state_update(member, before, after):
            
            # ignore movements from bots 
            if member.bot:
                return

            resources_path = os.path.abspath(
                                    os.path.join(
                                        os.path.dirname(__file__), '..',
                                        'resources'
                                    )
                                ).replace("\\", "/")

            mp3_file = resources_path + '/beans.mp3'
            audio_source = discord.FFmpegPCMAudio(mp3_file)

            # user has either joined channel or moved from one channel to another
            if before.channel != after.channel and after.channel: 

                # check if bot is connected 
                channel = await self.client.fetch_channel(after.channel.id)
                guild = channel.guild
                vc = core.voice.voice.check_voice_clients(self, guild)

                # check if targets exist for this guild
                # only connect if the target is connected to the voice channel
                if self.target_dict.get(channel.guild.id) is not None:
                    return

                # if no targets exist for this guild then join if any user joins
                if vc is None:
                    await channel.connect()
                    vc = self.client.voice_clients[0]
                else:
                    await vc.move_to(after.channel)
                
                # play the audio file
                core.voice.voice.speak_beans(self, vc, audio_source)

            # user has left the channel
            elif before.channel != after.channel and after.channel is None:
                # check if the bot is the only user in the channel
                channel = await self.client.fetch_channel(before.channel.id)
                guild = channel.guild
                vc = core.voice.voice.check_voice_clients(self, guild)
                if vc is not None:
                    bot_list = list(set([member.bot for member in channel.members]))
                    if False not in bot_list:
                        await vc.disconnect()
           
        @self.client.event
        async def on_message(message):
            # check if the message is a command
            if message.content.startswith(self.prefix):
                # Split the message into the command and its arguments
                parts = message.content.split()[1:]
                command = parts[0]
                args = parts[1:]

                # find the command in the parts array
                command_obj = [val for key, val in self.commands.items()
                               if command in key]

                if command_obj:
                    await command_obj[0].execute(message, args)

                logs.logger.info(f'targets: {self.target_dict}')

            # if message is not a command then check if it matches a trigger
            # word in alexisms
            else:
                # to prevent the bot from triggering itself if
                if message.author == self.client.user:
                    return

                # in a message someone might say multiple trigger words
                # e.g. Alex and shit
                # identify all trigger words that exist in a message
                trigger_words = [key for key in core.alexisms.phrases.keys()
                                 if key in message.content.lower()]

                for trigger_word in trigger_words:
                    responses = core.alexisms.phrases[trigger_word]
                    if isinstance(responses, list):
                        await message.channel.send(rand.choice(responses))

                    elif isinstance(responses, str):
                        await message.channel.send(responses)

                    else:
                        return

        self.client.run(self.token)
