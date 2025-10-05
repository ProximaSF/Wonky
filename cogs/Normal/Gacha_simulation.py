import disnake
from disnake.ext import commands
import random
import traceback
import asyncio

class Gacha_sim(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def WuWa_gacha(self, ctx):
        def random_generator():
            return random.random()

        def ten_pull():
            return [round(random_generator(), 3) for _ in range(10)]

        async def check5star():
            five_star_threshold = 0.008
            ten_pulls_list = ten_pull()
            five_star_count = sum(1 for value in ten_pulls_list if value <= five_star_threshold)

            if five_star_count != 0:
                msg = (f"**There was a 5 star, pulled {five_star_count}**\n"
                       f"Result: {ten_pulls_list}\n"
                       f"5 Star Rate: 0.8%")
            else:
                msg = (f"**Didn't pull a 5 star**\n"
                       f"Result: {ten_pulls_list}\n"
                       f"5 Star Rate: 0.8%")
            await ctx.send(msg)

        await check5star()

    @commands.command()
    async def gacha_sim(self, ctx):

        await ctx.send("**Gacha Simulator**\n"
                       "__Enter the following__:\n"
                       ":one:. 5 star drop rate (percentage)\n"
                       ":two:. Number of pulls you want to simulate (max 100 pulls).\n"
                       ":three:. If `0`, than enter number of 10 pulls\n\n"
                       "Example1: `0.08%-0-60` (60 ten pulls)\n"
                       "Example2: `0.34%-3` (3 pulls)")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        # Check if user input contain the right characters
        def contains_only_valid_chars(user_message_content):
            valid_chars = set("0123456789.%-")
            for char in user_message_content:
                if char not in valid_chars:
                    return False
            return True

        while True:
            try: # Handle errors
                try: # Handle no response
                    await asyncio.sleep(0.5)
                    msg = await asyncio.wait_for(self.client.wait_for('message', check=check), timeout=20.0)
                    user_message_content = msg.content

                    if contains_only_valid_chars(user_message_content):
                        user_msg_info_list = user_message_content.split("-")
                        # print(user_msg_info_list)
                        def random_generator():
                            return random.random()

                        async def single_pulls(drop_rate, num_pulls):
                            def pulls():
                                return [round(random_generator(), 3) for _ in range(num_pulls)]

                            five_star_threshold = drop_rate
                            ten_pulls_list = pulls()
                            five_star_count = sum(1 for value in ten_pulls_list if value <= five_star_threshold)

                            if five_star_count != 0:
                                msg = (f"**There was a 5 star, pulled {five_star_count}**\n"
                                       f"Result: {ten_pulls_list}\n"
                                       f"5 Star Rate: {drop_rate*100}%\n\n"
                                       f"Getting a 5 star in {num_pulls} pull(s) is **{(five_star_count/num_pulls) * 100}%** ")
                            else:
                                msg = (f"**Didn't pull a 5 star**\n"
                                       f"Result: {ten_pulls_list}\n"
                                       f"5 Star Rate: {drop_rate*100}%\n"
                                       f"Unlucky bud")
                            await ctx.send(msg)

                        async def multi_10_pulls(drop_rate, num_ten_pulls):
                            def ten_pulls():
                                return [round(random_generator(), 3) for _ in range(10)]

                            total_5_star_drop = 0
                            for i in range(num_ten_pulls):
                                ten_pull_list = ten_pulls()
                                five_star_count = sum(1 for value in ten_pull_list if value <= drop_rate)
                                total_5_star_drop += five_star_count

                            if total_5_star_drop != 0:
                                drop_rate_percentage = (total_5_star_drop/(10 * num_ten_pulls))*100
                                print(drop_rate_percentage)
                                msg = (f"**There was a 5 star, pulled {total_5_star_drop}**\n"
                                       f"5 Star Rate: {drop_rate*100}%\n\n"
                                       f"Getting multiple 5 stars in {10*num_ten_pulls} pull(s) is **{drop_rate_percentage}%** ")
                            else:
                                msg = (f"**Didn't pull a 5 star**\n"
                                       f"5 Star Rate: {drop_rate*100}%\n"
                                       f"Unlucky bud")
                            await ctx.send(msg)

                        if len(user_msg_info_list) == 2 and user_msg_info_list[1] != 0:
                            drop_rate = float(user_msg_info_list[0].replace("%", ''))
                            drop_rate = drop_rate/100
                            num_pulls = int(user_msg_info_list[1])
                            await single_pulls(drop_rate, num_pulls)
                            break
                        else:
                            drop_rate = float(user_msg_info_list[0].replace("%", ''))
                            drop_rate = drop_rate/100
                            num_ten_pulls = int(user_msg_info_list[2])
                            await multi_10_pulls(drop_rate, num_ten_pulls)
                            break
                    else:
                        await ctx.send("Please try again, make sure the drop-rate is in decimal and rest are integers")
                except asyncio.TimeoutError: # Break loop after a certain period
                    # await ctx.send("No response received within the timeout period")
                    break
            except Exception as error:
                error_info = traceback.format_exc()
                print(f"Error: {error}\n{error_info}")
def setup(client):
    client.add_cog(Gacha_sim(client))