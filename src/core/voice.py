import discord
class voice:
    def __init__(self, bot) -> None:
        self.bot = bot
    
    def detect(self):
        @self.client.event
        async def on_voice_state_update(self, member, before, after):
            
            # check that the id is not beans bot
            if member.id == 1054876494222078012:
                return

            # create new voice client 
            channel = await self.bot.client.fetch_channel(after.channel.id)
            
            # check if there is an existing voice connection
            if check_voice_client(self, after.guild):
                print("voice_client for guild exists")
            else:
                await channel.connect()




        # check for voice client connections
        def check_voice_client(self, guild):
            voice_clients = discord.utils.get(self.bot.client.voice_clients)
            if voice_clients:
                for vc in voice_clients:
                    if vc.guild.id == guild.id:
                        return True
            return False

            


