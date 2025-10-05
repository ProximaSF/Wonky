from discord_webhook import DiscordWebhook, DiscordEmbed
from disnake.ext import commands

class Webhook(commands.Cog):
    def __init__(self):
        self.webhook_url = ''

    def webhook_embed(self, title, message_description):
        webhook = DiscordWebhook(url=self.webhook_url)
        embed = DiscordEmbed(title=title, description=message_description)
        webhook.add_embed(embed)
        webhook.execute()
        return

def setup(client):
    client.add_cog(Webhook())