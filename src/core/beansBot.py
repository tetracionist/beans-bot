import discord, core.alexisms, random as rand

class beansBot():
    def __init__(self: object, token: str, intents: object, commands: dict, prefix='!bb'):
        self.token = token
        self.intents = intents
        self.client = discord.Client(intents=intents)
        self.prefix = prefix

        # define commands 
        self.commands = commands
            
    
    def start(self):
        @self.client.event
        async def on_ready():
            print("ready")
        
        
        @self.client.event
        async def on_message(message):

            print(message)

            # check if the message is a command
            if message.content.startswith(self.prefix):
                print("commad")

            # if message is not a command then check if it matches a trigger word in alexisms
            else:
                # to prevent the bot from triggering itself if it finds a response in 
                if message.author == self.client.user:
                    return

                # in a message someone might say multiple trigger words: e.g. Alex and shit 
                # identify all trigger words that exist in a message 
                trigger_words = [key for key in core.alexisms.phrases.keys() if key in message.content.lower()]  

                for trigger_word in trigger_words: 
                    responses = core.alexisms.phrases[trigger_word]
                    if isinstance(responses, list):
                        await message.channel.send(rand.choice(responses)) 

                    elif isinstance(responses, str):
                        await message.channel.send(responses) 

                    else:
                        return
        
        self.client.run(self.token) 






