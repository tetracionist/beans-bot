import discord, random as rand 
import core.alexisms, core.voice
import logs

class beansBot:
    def __init__(self: object, token: str, intents: object, prefix='!bb'):
        self.token = token
        self.intents = intents
        self.client = discord.Client(intents=intents)
        self.prefix = prefix
        self.target_dict = {}

        # define commands 
        self.commands = {"ping": core.commands.PingCommand(self),
                         "target": core.commands.TargetCommand(self)}
        
        
        
            
    
    def start(self):
        @self.client.event
        async def on_ready():
            logs.logger.info('Log In Successful')

        @self.client.event
        async def on_voice_state_update(member, before, after):
            
            # get channel
            channel = after.channel

            vc = core.voice.voice.check_voice_clients(self, channel.guild)
            if vc == None:
                await channel.connect()

            
        
        @self.client.event
        async def on_message(message):

            #print(message)

            # check if the message is a command
            if message.content.startswith(self.prefix):
                # Split the message into the command and its arguments
                parts = message.content.split()[1:]
                command = parts[0]
                args  = parts[1:]

                # find the command in the parts array
                command_obj = [val for key, val in self.commands.items() if command in key]

                if command_obj:
                    await command_obj[0].execute(message, args)
            
                logs.logger.info(f'targets: {self.target_dict}')



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






