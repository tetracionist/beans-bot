class voice:
    def __init__(self, bot) -> None:
        self.bot = bot

    def check_voice_clients(self, guild):
        voice_clients = self.client.voice_clients
        if voice_clients:
            for vc in voice_clients:
                if vc.guild.id == guild.id:
                    return vc
        return None
