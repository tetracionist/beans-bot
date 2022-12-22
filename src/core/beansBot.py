import discord 
class beansBot():
    def __init__(self, token):
        self.token = token
        self.client = discord.Client()    

    async def start(self):

        self.client.run(self.token)

        @self.client.event
        async def on_ready():
            print(f"{self.client.user.name} is connected")