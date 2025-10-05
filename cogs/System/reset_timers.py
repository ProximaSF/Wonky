from disnake.ext import commands
import asyncio
import datetime
import os
import ast  # convert string dict into a usable dict

from cogs.System.PointsAdjust import Adjust_WobbleBBits
Instance_WobbleBits = Adjust_WobbleBBits()

def im_server_status_string_to_dictionary(guild_id):
    file_path = f'txt/ServerSettings/{guild_id}/{guild_id}.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for line in lines:
            if "I'm Time Reset:" in line:
                start_dic = line.find('{')
                dic_string = line[start_dic:]
                return ast.literal_eval(dic_string)

def read_im_timer_server_setting_values(guild_id):
    server_joke_bool = []
    dictionary = im_server_status_string_to_dictionary(guild_id)
    for keys in dictionary:
        server_joke_bool.append(dictionary[keys])
    return server_joke_bool

class reset_timers(commands.Cog):
    def __init__(self, client):
        self.client = client

        # Schedule daily resets at midnight and noon
        self.client.loop.create_task(self.daily_reset_loop(0, 12))  # Midnight and Noon

    async def daily_reset_loop(self, hour1, hour2):
        while True:
            now = datetime.datetime.now()
            current_hour = now.hour
            next_reset_time = None

            # Determine the next reset time based on current time
            if current_hour < hour1:
                next_reset_time = datetime.datetime(now.year, now.month, now.day, hour1, 0, 0)
            elif current_hour < hour2:
                next_reset_time = datetime.datetime(now.year, now.month, now.day, hour2, 0, 0)
            else:
                # Already passed both times, reset tomorrow
                next_reset_time = datetime.datetime(now.year, now.month, now.day, hour1, 0, 0) + datetime.timedelta(days=1)

            # Calculate time until next reset
            delta = next_reset_time - now
            await asyncio.sleep(delta.total_seconds())

            # Perform reset actions
            await self.perform_daily_reset()

    async def perform_daily_reset(self):
        # Implement your reset actions here
        print("Performing daily reset at", datetime.datetime.now())

        # Example: Resetting some data
        for guild in self.client.guilds:
            guild_id = guild.id
            im_status = read_im_timer_server_setting_values(guild_id)
            if im_status[0]:
                file_path = f'txt/ServerSettings/{guild_id}/{guild_id}.txt'
                if os.path.exists(file_path):
                    with open(file_path, 'r+') as file:
                        lines = file.readlines()
                        file.seek(0)
                        for line in lines:
                            if "I'm Time Reset:" in line:
                                line = "I'm Time Reset: {'enable': True, 'rested': True}"
                            file.write(line)
                        file.truncate()

    @commands.has_any_role("admin", "Admin")
    @commands.command()
    async def EstatusIm(self, ctx):
        try:
            await ctx.send("Type **true** to enable I'm joke reply or **false** to disable.")

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            guild_id = ctx.guild.id
            file_path = f"txt/ServerSettings/{guild_id}/{guild_id}.txt"
            msg = await self.client.wait_for('message', check=check)
            if msg.content.casefold() == "true":
                with open(file_path, 'r+') as file:
                    lines = file.readlines()
                    file.seek(0)
                    for line in lines:
                        if "I'm Time Reset:" in line:
                            line = "I'm Time Reset: {'enable': True, 'rested': True}"
                        file.write(line)
                    file.truncate()

            elif msg.content.casefold() == "false":
                with open(file_path, 'r+') as file:
                    lines = file.readlines()
                    file.seek(0)
                    for line in lines:
                        if "I'm Time Reset:" in line:
                            line = "I'm Time Reset: {'enable': False, 'rested': False}"
                        file.write(line)
                    file.truncate()
        except Exception as error:
            print(error)

def setup(client):
    client.add_cog(reset_timers(client))