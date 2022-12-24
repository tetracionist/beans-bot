class Command:
    def __init__(self, bot, name, description):
        self.bot = bot
        self.name = name
        self.description = description

class PingCommand(Command):
    def __init__(self, bot):
        super().__init__(bot, 'ping', 'Sends a pong message')

    async def execute(self, message, args):
        await message.channel.send('Pong!')


class TargetCommand(Command):
    def __init__(self, bot):
        super().__init__(bot, 'target', 'Chooses a guild member to target')
    
    async def execute(self, message, args):

        if 'clear' in args:
            return

        # this needs to be done on a guild by guild basis
        # think about how we might store this data

        # find user ids in the args


        # first check if user is in guild
        guild = self.bot.client.get_guild(message.guild.id)
        guild_members = [guild_member.id for guild_member in guild.members]
        targets = [arg for arg in args if arg in guild_members]



        print(targets)