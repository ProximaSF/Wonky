import asyncio
import os

import disnake
import random
from disnake.ext import commands

from cogs.Normal.Hangman import Hangman
from cogs.Normal.Wordle import Wordle
from cogs.Normal.Tick_Tac_Toe import Tic_Tac_Toe
from cogs.Normal.Trivia import Trivia


class Word_Games(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.wordle = True
        self.ngg = True
        self.ttt = True
        self.hangman = True
        self.pick_game = []


    @commands.has_any_role("Admin")
    @commands.command()
    async def stop_playground(self, ctx):
        guild_id = ctx.guild.id
        file_path = f"txt/ServerSettings/{guild_id}/{guild_id}.txt"

        def read_word_game_status():
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    for line in file:
                        if "Word Games:" in line:
                            return line.strip().split(":")[1].strip().lower()

        def turn_WG_to_false():
            with open(file_path, 'r') as f:
                lines = f.readlines()
            with open(file_path, "w") as f:
                for line in lines:
                    if "Word Games:" in line:
                        line = "Word Games: false\n"
                    f.write(line)

        if read_word_game_status() == "true":
            turn_WG_to_false()
            await ctx.send("**All games has been canceled**")
        else:
            await ctx.send("**No game is running.**", delete_after=4)

    @commands.has_any_role("Admin")
    @commands.command()
    async def start_playground(self, ctx):
        guild_id = ctx.guild.id
        file_path = f"txt/ServerSettings/{guild_id}/{guild_id}.txt"

        def read_word_game_status():
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    for line in file:
                        if "Word Games:" in line:
                            return line.strip().split(":")[1].strip().lower()

        def turn_WG_to_true():
            with open(file_path, 'r') as f:
                lines = f.readlines()
            with open(file_path, "w") as f:
                for line in lines:
                    if "Word Games:" in line:
                        line = "Word Games: true\n"
                    f.write(line)
        def game_picker():
            if not self.pick_game:
                self.pick_game += ["wordle"] * 1
                self.pick_game += ["hangman"] * 1
                self.pick_game += ["trivia"] * 3
            picker = random.choice(self.pick_game)
            self.pick_game.remove(picker)
            return picker

        if read_word_game_status() == "false":
            turn_WG_to_true()
            while True:
                await asyncio.sleep(2)
                if read_word_game_status() == "true":
                    game = game_picker()
                    # print(game)

                    if game == "wordle":
                        wordle_instance = Wordle(self.client)
                        await wordle_instance.wordle(ctx)
                        await asyncio.sleep(0)

                    elif game == "trivia":
                        trivia_instance = Trivia(self.client)
                        await trivia_instance.trivia_auto(ctx)
                        await asyncio.sleep(0)

                    elif game == "ttt":
                        tic_tac_to_instance = Tic_Tac_Toe(self.client)
                        await tic_tac_to_instance.TTT_auto(ctx)
                        await asyncio.sleep(0)

                    elif game == "hangman":
                        hangman_instance = Hangman(self.client)
                        await hangman_instance.hangman(ctx)
                        await asyncio.sleep(0)  # Help detect if the loop should end or not
                else:
                    break
        else:
            await ctx.send("Word games already running")

    @commands.command()
    async def playground_help(self, ctx):
        total_pages = "3"

        page1 = embed = disnake.Embed(title=f'Wordle Command Help', color=disnake.Color.orange())
        embed.add_field(name='**How to play**', value=
        f"\n1️⃣. **Bold** letter represent correct letter in the correct position.\n"
        f"\n2️⃣. __Underline__ letter represent correct letter but wrong position.\n"
        f"\n3️⃣. ~~Struck-through~~ letters represent the absence of that letter.", inline=False)
        embed.set_footer(text=f'Page 1/{total_pages}')

        page2 = embed = disnake.Embed(title=f'Wordle Command Help', color=disnake.Color.orange())
        embed.add_field(name="Commands",
                        value='⚫ When using **&wordle**, type the command in a empty channel you wish the bot to run in.\n'
                              '\n⚫ Use **&stop_wordle** to stop the **^wordle** command entirely.\n'
                              '\n⚫ All wordle commands in this page require admin roles.', inline=False)
        embed.set_footer(text=f'Page 2/{total_pages}')

        page3 = embed = disnake.Embed(title=f'Wordle Command Help', color=disnake.Color.orange())
        embed.add_field(name="WobbleBits",
                        value='⚫ To see how many WobbleBits you or others have use **&info @user**.\n'
                              '\n⚫ WobbleBits is based on the number of __total WobbleBits(20)__/__attempts the word '
                              'as successfully entered__ rounded to the lowest integer.\n', inline=False)
        embed.set_footer(text=f'Page 3/{total_pages}')

        pages = [page1, page2, page3]

        message = await ctx.send(embed=page1)
        await message.add_reaction('⏮')
        await message.add_reaction('◀')
        await message.add_reaction('▶')
        await message.add_reaction('⏭')

        def check(reaction, user):
            return user == ctx.author and reaction.message == message

        i = 0
        reaction = None

        while True:
            if str(reaction) == '⏮':
                i = 0
                await message.edit(embed=pages[i])
            elif str(reaction) == '◀':
                if i > 0:
                    i -= 1
                    await message.edit(embed=pages[i])
            elif str(reaction) == '▶':
                if i < 5:
                    i += 1
                    await message.edit(embed=pages[i])
            elif str(reaction) == '⏭':
                i = 2
                await message.edit(embed=pages[i])

            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=120.0, check=check)
                await message.remove_reaction(reaction, user)
            except:
                break
        await message.edit(embed=page1)
        await message.clear_reactions()


def setup(client):
    client.add_cog(Word_Games(client))  # bot.add_cog(mech(bot)) is the name of the cog "mech" must match line 8
