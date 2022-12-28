import re


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


class target_command(command):
    def __init__(self, bot):
        super().__init__(bot, 'target', 'Chooses a guild member to target')

    async def execute(self, message, args):

        if 'clear' in args:
            return

        # this needs to be done on a guild by guild basis
        # think about how we might store this data
        users = [int(''.join(re.findall(r'[0-9]', arg)).strip())
                 for arg in args]

        # first check if user is in guild
        guild = self.bot.client.get_guild(message.guild.id)
        guild_members = [guild_member.id for guild_member in guild.members]
        targets = [arg for arg in users if arg in guild_members]

        if not targets:
            await message.channel.send('Target is not in this server')
            return

        self.bot.target_dict[guild.id] = targets

        for target in targets:
            user = self.bot.client.get_user(target)

            await user.send('Get Rekt')
