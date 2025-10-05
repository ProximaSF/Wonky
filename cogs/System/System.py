import disnake
from disnake.ext import commands
from disnake import Interaction
from disnake import FFmpegPCMAudio
from disnake import Member

import asyncio
import random
import re
import giphy_client
from giphy_client.rest import ApiException

class System(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.has_any_role("admin", "Admin")
    @commands.command(name="reminder")
    async def _reminder(self, ctx):
        await ctx.send(
            f"**How many minutes/hours do you want to set the reminder?**\nMake sure you have the value for the "
            f"period, than press space and type `'hour or hours'` to count in hour or `'mins'` to count in "
            f"minutes\n\n "
            f"Example: 2 hour or 2 hours or 2 mins\nWRONG: 2hour or 2hours or 2mins - there isn't any space\n"
            f"__Just type a random letter to cancel command__", delete_after=30)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await self.client.wait_for('message', check=check)
        if 'mins' in msg.content or 'min' in msg.content:
            for character in msg.content.split():
                if character.isdigit():
                    value = int(character)
                    await ctx.send("What is your message?", delete_after=30)
                    msg = await self.client.wait_for('message', check=check)
                    user_message = msg.content

                    await ctx.send(f"Is this the message you want: **{user_message}**? If so do you want to "
                                   f"continue?\n`yes` or `no`?", delete_after=30)
                    msg = await self.client.wait_for('message', check=check)
                    if 'yes' in msg.content:

                        await ctx.send("Which channel do you want the message?", delete_after=30)

                        def check(msg):
                            return len(
                                msg.channel_mentions) != 0 and msg.channel == ctx.channel and ctx.author == msg.author

                        msg = await self.client.wait_for("message", check=check)
                        await ctx.send(
                            f"Your message for '{user_message} to {msg.content}' will send in `{value} mins`")
                        channel_id = msg.channel_mentions[0].id
                        channel = self.client.get_channel(channel_id)
                        await asyncio.sleep(value * 60)
                        await channel.send(f"{user_message}")
                    else:
                        await ctx.send("You said no", delete_after=30)
                        break
        elif 'hours' in msg.content or 'hour' in msg.content:
            for character in msg.content.split():
                if character.isdigit():
                    value = int(character)
                    await ctx.send("What is your message?", delete_after=15)
                    msg = await self.client.wait_for('message')
                    user_message = msg.content

                    await ctx.send(f"Is this the message you want: **{user_message}**? If so do you want to "
                                   f"continue?\n`yes` or `no`?", delete_after=15)
                    msg = await self.client.wait_for('message', check=check)
                    if 'yes' in msg.content:

                        await ctx.send("Which channel do you want the message?", delete_after=15)

                        def check(msg):
                            return len(
                                msg.channel_mentions) != 0 and msg.channel == ctx.channel and ctx.author == msg.author

                        msg = await self.client.wait_for("message", check=check)
                        await ctx.send(f"Your message for {user_message} to {msg.content} will send in `{value} hours`")
                        channel_id = msg.channel_mentions[0].id
                        channel = self.client.get_channel(channel_id)
                        await asyncio.sleep(value * 3600)
                        await channel.send(f"{user_message}")
                    else:
                        await ctx.send("You said no", delete_after=15)
                        break

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx):
        await ctx.send(
            f"How many messages do you want to clear?\n\nBTW: &cleaar, this message and your value message will "
            f"automatically be deleted\nType a random letter or symbol to stop")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        msg = await self.client.wait_for("message", check=check)
        for character in msg.content.split():
            if character.isdigit():
                value = int(character)
                await ctx.channel.purge(limit=value + 3)
                await ctx.send(f"**{value} messages has been deleted**")


    @commands.command()
    async def invite(self, ctx):
        await ctx.send(
            f"https://discord.com/api/oauth2/authorize?client_id=985090928429649920&permissions=414464800838&scope=bot")

    @commands.has_any_role("ProximaSF")
    @commands.command()
    async def load(self, ctx, extension):
        try:
            self.client.load_extension(f"cogs.{extension}")
            print(f"Loaded {extension}.\n")
            await ctx.send(f"Loaded {extension}")
        except Exception as error:
            print(f"{extension} could not be loaded. [{error}]")
            await ctx.send(f"{extension} could not be loaded. [{error}]")

    @commands.has_any_role("ProximaSF")
    @commands.command()
    async def unload(self, ctx, extension):
        try:
            self.client.unload_extension(f"cogs.{extension}")
            print(f"Unloaded {extension}.\n")
            await ctx.send(f"Unloaded {extension}")
        except Exception as error:
            print(f"{extension} could not be unloaded. [{error}]")
            await ctx.send(f"{extension} could not be unloaded. [{error}]")

def setup(client):
    client.add_cog(System(client))