import re
import os
import discord
from core.voice import voice
import core.alexisms
import asyncio
import random as rand
from sympy import parse_expr, simplify, expand, integrate


class command:
    def __init__(self, bot, name, description):
        self.bot = bot
        self.name = name
        self.description = description


class ping_command(command):
    def __init__(self, bot):
        super().__init__(bot, 'ping', 'Sends a pong message')

    async def execute(self, message, args):
        await message.channel.send('Pong!')


class say_command(command):
    def __init__(self, bot):
        super().__init__(bot, 'say', 'sends message to text channel')

    async def execute(self, message, args):
        # send a random alexism
        if args[0] == 'alexism':
            random_alexism = rand.choice(list(core.alexisms.phrases.values()))

            if isinstance(random_alexism, list):
                await message.channel.send(rand.choice(random_alexism))

            elif isinstance(random_alexism, str):
                await message.channel.send(random_alexism)


class speak_command(command):
    def __init__(self, bot):
        super().__init__(bot, 'speak', 'speaks in voice')

    async def execute(self, message, args):

        # check for voice client in guild
        vc = voice.check_voice_clients(self.bot, message.guild)
        member = message.author
        member_voice_state = member.voice

        # connect to the same channel as the member and say beans
        if vc is None:
            await member_voice_state.channel.connect()
            vc = self.bot.client.voice_clients[0]

        # otherwise move_to the channel
        else:
            await vc.move_to(member_voice_state.channel)

        resources_path = os.path.abspath(
                                    os.path.join(
                                        os.path.dirname(__file__), '..',
                                        'resources'
                                    )
                                ).replace("\\", "/")

        if args[0] == 'alexism':
            # choose a random alexism for the folder
            alexism_dir = f"{resources_path}/alexisms"
            alexism_file = rand.choice(os.listdir(alexism_dir))

            mp3_file = f"{alexism_dir}/{alexism_file}"
            audio_source = discord.FFmpegPCMAudio(mp3_file)
            # play beans
            while vc.is_playing():
                await asyncio.sleep(1)

            vc.play(audio_source, after=None)

        else:
            for arg in args:
                mp3_file = resources_path + '/'+arg+'.mp3'
                audio_source = discord.FFmpegPCMAudio(mp3_file)

                # play beans
                while vc.is_playing():
                    await asyncio.sleep(1)

                vc.play(audio_source, after=None)


class do_maths_command(command):
    def __init__(self, bot):
        super().__init__(bot, 'do_maths', 'Does mathematical calculation')

    async def execute(self, message, args):
        await message.channel.send("_I'm Doing Maaaaaths!_")
        expr = parse_expr(' '.join(args[1:]))

        match args[0]:
            case 'expand':
                op = expand(expr)
            case 'integrate':
                op = integrate(expr)
            case _:
                op = expr
    
        await message.channel.send(simplify(op))


class target_command(command):
    def __init__(self, bot):
        super().__init__(bot, 'target', 'Chooses a guild member to target')

    async def execute(self, message, args):
        guild = self.bot.client.get_guild(message.guild.id)
        if 'show' in args:

            if self.bot.target_dict.get(guild.id) is None:
                await message.channel.send("There are no active targets")
                return

            guild_targets = self.bot.target_dict[guild.id]

            await message.channel.send("Targeting:")
            for guild_member in guild_targets:
                await message.channel.send(
                    self.bot.client.get_user(guild_member).mention
                )
            return

        if 'clear' in args:
            self.bot.target_dict.pop(guild.id, None)
            await message.channel.send(f'Cleared targets for {guild.name}')
            return

        # this needs to be done on a guild by guild basis
        # think about how we might store this data
        users = [int(''.join(re.findall(r'[0-9]', arg)).strip())
                 for arg in args]

        # first check if user is in guild
        guild_members = [guild_member.id for guild_member in guild.members]
        targets = [arg for arg in users if arg in guild_members]

        if not targets:
            await message.channel.send('Target is not in this server')
            return

        self.bot.target_dict[guild.id] = targets

        for target in targets:
            user = self.bot.client.get_user(target)

            await user.send('Get Rekt')
