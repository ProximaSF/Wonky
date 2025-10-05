import os
import asyncio
import disnake
import disnake.utils
from disnake.ext import commands
import traceback
import random

from cogs.System.PointsAdjust import Adjust_WobbleBBits
Instance_ValueAdjust = Adjust_WobbleBBits()

class Num_Guessing_Game(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.max_num = None
        self.random_num = None
        self.isTrue = True
        self.msg = None

        self.isTrue2 = True
        self.num_of_hints = 5
        self.msg2 = None  # to detect reaction
        self.user_guess = None
        self.message_id = None

    async def num_guessing_game(self, ctx):
        guild_id = ctx.guild.id
        file_path = f"txt/ServerSettings/{guild_id}/{guild_id}.txt"

        def read_word_game_status():
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    for line in file:
                        if "Word Games:" in line:
                            return line.strip().split(":")[1].strip().lower()

        def random_gen_number():
            self.max_num = random.randint(30, 100)
            self.random_num = random.randint(1, self.max_num)

        async def add_higher_reactions():
            await self.msg.add_reaction("⬆️")

        async def add_lower_reactions():
            await self.msg.add_reaction("⬇️")

        async def check_input():
            def check(msg):
                return msg.channel == ctx.channel

            while self.isTrue:
                try:
                    if read_word_game_status() == "false":
                        break

                    msg = await self.client.wait_for('message', check=check)
                    self.msg = msg
                    if msg.content.casefold() == "-stop":
                        await ctx.send(f"The number was {self.random_num}")
                        self.isTrue = False

                    elif int(msg.content) == self.random_num:
                        winner = msg.author.mention
                        await ctx.send(f"{winner} found the value {self.random_num}")
                        self.isTrue = False

                    elif int(msg.content) < self.random_num:
                        await add_higher_reactions()

                    elif int(msg.content) > self.random_num:
                        await add_lower_reactions()
                except ValueError:
                    pass

        async def start_msg():
            random_gen_number()
            ngg_info = (
                f":regional_indicator_n:  :regional_indicator_u:  :regional_indicator_m:  :regional_indicator_b:  :regional_indicator_e:  :regional_indicator_r:"
                "\n---------------------------------------------------------"
                f"\nGuess the number between ({1} - {self.max_num})"
                "\n---------------------------------------------------------")
            await ctx.send(ngg_info)
            await asyncio.sleep(0.5)
            await check_input()

        await start_msg()

    @commands.command()
    async def NGG(self, ctx):
        try:
            def random_gen_number():
                self.max_num = random.randint(30, 200)
                self.random_num = random.randint(1, self.max_num)
                #print(self.random_num)

            # remove all ''' to allow hint reaction
            async def remove_reaction():
                old_message = await ctx.channel.fetch_message(self.message_id)
                old_emoji = self.client.get_emoji(1198887331990618153)
                await old_message.remove_reaction(old_emoji, self.client.user)
                return

            async def check_input():
                def check(msg):
                    return msg.channel == ctx.channel

                while self.isTrue2:
                    try:
                        msg = await self.client.wait_for('message', check=check)

                        if msg.content.casefold() == "-stop":
                            await ctx.send(f"The number was {self.random_num}")
                            self.isTrue2 = False
                            break

                        if msg.content.isdigit():
                            if self.message_id is None:
                                pass
                            else:
                                await remove_reaction()
                            self.msg2 = msg
                            self.message_id = msg.id
                            self.user_guess = int(msg.content)
                            # print(self.user_msg_id)'''

                            if int(msg.content) == self.random_num:
                                winner = msg.author.mention
                                await ctx.send(f"{winner} found the value **{self.random_num}**")
                                Instance_ValueAdjust.add_WobbleBits(msg.author.id, 5)
                                # self.num_of_hints = 5
                                await asyncio.sleep(2)
                                await start_msg()

                            elif (int(msg.content) < self.random_num) or (int(msg.content) > self.random_num):
                                '''if self.num_of_hints <= 0:'''
                                gen_ran_num = random.randint(1, 10)
                                extra_chance = 7
                                if gen_ran_num <= extra_chance:
                                    if self.user_guess < self.random_num:
                                        await self.msg2.add_reaction("⬆️")
                                    else:
                                        await self.msg2.add_reaction("⬇️")
                                else:
                                    await msg.add_reaction("❌")
                                '''else:
                                    emoji = self.client.get_emoji(1198887331990618153)
                                    await msg.add_reaction(emoji)'''
                            '''else:
                                pass'''
                    except ValueError:
                        pass

            async def start_msg():
                random_gen_number()
                ngg_info = (
                    f":regional_indicator_n:  :regional_indicator_u:  :regional_indicator_m:  :regional_indicator_b:  :regional_indicator_e:  :regional_indicator_r:"
                    "\n---------------------------------------------------------"
                    f"\nGuess the number between **{1} - {self.max_num}**"
                    # f"\nReact to the bulb for a hint `5 hints per match` "
                    "\n---------------------------------------------------------")
                await ctx.send(ngg_info)
                await asyncio.sleep(0.5)
                await check_input()

            await start_msg()
        except Exception as error:
            error_info = traceback.format_exc()
            await ctx.send(f"Error: {error}")
            print(f"Error: {error}\n{error_info}")
            return
    '''
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Handle reactions added to messages."""
        # Ignore reactions added by the bot itself
        if user.bot:
            return

        member = disnake.utils.get(reaction.message.guild.members, id=user.id)

        # Hint reaction
        hint_emoji_id = 1198887331990618153
        hint_emoji = self.client.get_emoji(hint_emoji_id)

        if reaction.emoji == hint_emoji and reaction.message.id == self.message_id:
            if self.num_of_hints <= 0:
                await reaction.message.channel.send(f"Used up all the hint for this session")

            else:
                self.num_of_hints -= 1
                if self.user_guess < self.random_num:
                    await self.msg2.add_reaction("⬆️")
                    await reaction.message.remove_reaction(reaction, user)
                    await reaction.message.remove_reaction(reaction, reaction.message.guild.me)

                else:
                    await self.msg2.add_reaction("⬇️")
                    await reaction.message.remove_reaction(reaction, user)
                    await reaction.message.remove_reaction(reaction, reaction.message.guild.me)
        return
    '''

def setup(client):
    client.add_cog(Num_Guessing_Game(client))