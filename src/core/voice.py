class voice:
    def __init__(self, bot) -> None:
        self.bot = bot

    def check_voice_clients(self, guild):
        voice_client = [vc for vc in self.client.voice_clients
                        if vc.guild.id == guild.id]
        if voice_client:
            return voice_client[0]
        else:
            return None
