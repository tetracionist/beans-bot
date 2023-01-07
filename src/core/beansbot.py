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

            # if the target is empty then join the voice channel when any user
            # joins the voice channel
            # only disconnect if voice channel contains beans bot

            # if the target is not empty then join voice channel
            # if any of the target users join the voice channel
            # if they are speaking play the mp3 file
            # if all targets disconnect then disconnect

            channel = await self.client.fetch_channel(after.channel.id)
            guild = channel.guild
            vc = core.voice.voice.check_voice_clients(self, guild)

            if self.target_dict.get(channel.guild.id) is not None:
                if member.id in self.target_dict[channel.guild.id]:
                    if vc is None:
                        await channel.connect()
                        vc = self.client.voice_clients[0]

                    elif before.channel != after.channel and after.channel:
                        await vc.move_to(after.channel)

                    if not after.mute:
                        # in the event that the user clears targets it removes
                        # the key
                        while self.target_dict.get(channel.guild.id) is not None:
                            audio_source = discord.FFmpegPCMAudio(mp3_file)
                            vc.play(audio_source, after=None)
                            while vc.is_playing():
                                await asyncio.sleep(1)

            else:

                if vc is None:
                    await channel.connect()
                    vc = self.client.voice_clients[0]

                elif before.channel != after.channel and after.channel:
                    await vc.move_to(after.channel)

                if vc.is_playing():
                    vc.stop()

                vc.play(audio_source, after=None)

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
