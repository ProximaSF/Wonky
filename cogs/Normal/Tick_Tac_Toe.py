from disnake.ext import commands
import disnake
import traceback
import os
import random
import time


class Tic_Tac_Toe(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.possible_wins = {1: [1, 2, 3], 2: [4, 5, 6],
                              3: [7, 8, 9], 4: [1, 4, 7],
                              5: [2, 5, 8], 6: [3, 6, 9],
                              7: [1, 5, 9], 8: [3, 5, 7]}

        self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h, self.i = "1", "2", "3", "4", "5", "6", "7", "8", "9"
        self.location = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.user1_input_list = []
        self.user2_input_list = []
        self.player_name = "Player 1"
        self.isTrue = True
        # ----------------------------------------------
        # For command TTT
        self.a2, self.b2, self.c2, self.d2, self.e2, self.f2, self.g2, self.h2, self.i2 = "1", "2", "3", "4", "5", "6", "7", "8", "9"
        self.location2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.real_player_input_list = []
        self.bot_input_list = []
        self.player_name2 = "Your turn"
        self.footer_message = ''
        self.isTrue2 = True
        self.game_board = None

    async def TTT_auto(self, ctx):
        guild_id = ctx.guild.id
        file_path = f"txt/ServerSettings/{guild_id}/{guild_id}.txt"

        def read_word_game_status():
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    for line in file:
                        if "Word Games:" in line:
                            return line.strip().split(":")[1].strip().lower()

        async def print_game_board():
            game_board = (
                f" {self.a}   |   {self.b}   |   {self.c}\n"
                f" --------\n"
                f" {self.d}   |   {self.e}   |   {self.f}\n"
                f" --------\n"
                f" {self.g}   |   {self.h}   |   {self.i} "
            )
            embed = disnake.Embed(title="Tic-Tac-Toe")
            embed.add_field(name='', value=f"{game_board}")
            embed.set_footer(text=f"{self.player_name}'s turn")
            await ctx.send(embed=embed)

        async def check_for_winner():
            if len(self.location) == 0:
                await ctx.send("It was a tie, no one wins.")
                self.isTrue = False
                return False
            else:
                for i in self.possible_wins:
                    result = all(i in self.user1_input_list for i in self.possible_wins[i])
                    if result:
                        await ctx.send(f"**Player 1 wins!**")
                        self.isTrue = False
                        return False

                for i in self.possible_wins:
                    result = all(i in self.user2_input_list for i in self.possible_wins[i])
                    if result:
                        await ctx.send(f"**Player 2 wins!**")
                        self.isTrue = False
                        return False

        def remove_from_list(remove_val_from_list):
            if remove_val_from_list in self.location:
                self.location.remove(remove_val_from_list)
            else:
                return

        async def user1_input():
            def check(msg):
                return msg.channel == ctx.channel

            if not self.isTrue:
                return
            while True:
                try:
                    msg = await self.client.wait_for('message', check=check)
                    if msg.content.casefold() == '-stop':
                        embed = disnake.Embed(title="**Player 2 win**")
                        await ctx.send(embed=embed)
                        self.isTrue = False
                        return
                    user1_msg_int = int(msg.content)
                    await user1(user1_msg_int)
                    return user1_msg_int
                except ValueError:
                    pass
                    # await ctx.send("Enter a number only", delete_after=3)

        async def user2_input():
            def check(msg):
                return msg.channel == ctx.channel

            if not self.isTrue:
                return
            while True:
                try:
                    msg = await self.client.wait_for('message', check=check)
                    if msg.content.casefold() == '-stop':
                        embed = disnake.Embed(title="**Player 1 win**")
                        await ctx.send(embed=embed)
                        self.isTrue = False
                        return
                    user2_msg_int = int(msg.content)
                    await user2(user2_msg_int)
                    return user2_msg_int
                except ValueError:
                    pass
                    # await ctx.send("Enter a number only", delete_after=3)

        async def user1(user_1):
            if user_1 in self.location:
                if user_1 == 1:
                    self.a = "**X**"
                elif user_1 == 2:
                    self.b = "**X**"
                elif user_1 == 3:
                    self.c = "**X**"
                elif user_1 == 4:
                    self.d = "**X**"
                elif user_1 == 5:
                    self.e = "**X**"
                elif user_1 == 6:
                    self.f = "**X**"
                elif user_1 == 7:
                    self.g = "**X**"
                elif user_1 == 8:
                    self.h = "**X**"
                elif user_1 == 9:
                    self.i = "**X**"
                remove_val_from_list = user_1
                self.user1_input_list.append(user_1)
                remove_from_list(remove_val_from_list)
                self.player_name = 'Player 2'
                await print_game_board()
                # print(f"User1: {self.user1_input_list}")

                if await check_for_winner():
                    return
            else:
                await ctx.send("Position is already taken", delete_after=4)
                await user1_input()

        async def user2(user_2):
            if user_2 in self.location:
                if user_2 == 1:
                    self.a = "**O**"
                elif user_2 == 2:
                    self.b = "**O**"
                elif user_2 == 3:
                    self.c = "**O**"
                elif user_2 == 4:
                    self.d = "**O**"
                elif user_2 == 5:
                    self.e = "**O**"
                elif user_2 == 6:
                    self.f = "**O**"
                elif user_2 == 7:
                    self.g = "**O**"
                elif user_2 == 8:
                    self.h = "**O**"
                elif user_2 == 9:
                    self.i = "**O**"
                remove_val_from_list = user_2
                self.user2_input_list.append(user_2)
                remove_from_list(remove_val_from_list)
                self.player_name = 'Player 1'
                await print_game_board()
                # print(f"User1: {self.user2_input_list}")

                if await check_for_winner():
                    return
            else:
                await ctx.send("Position is already taken", delete_after=4)
                await user2_input()

        async def user_input():
            while self.isTrue:
                if read_word_game_status() == "false":
                    break
                while self.isTrue:
                    try:
                        await user1_input()
                        # print(self.location)

                        if not self.isTrue:
                            break

                        await user2_input()
                        # print(self.location)

                    except Exception as error:
                        error_info = traceback.format_exc()
                        print(f"Error: {error}\n{error_info}")
                        return

        await print_game_board()
        await user_input()

    @commands.command()
    async def TTT(self, ctx):

        try:
            def reset_game_values():
                self.a2, self.b2, self.c2, self.d2, self.e2, self.f2, self.g2, self.h2, self.i2 = "1", "2", "3", "4", "5", "6", "7", "8", "9"
                self.location2 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                self.real_player_input_list = []
                self.bot_input_list = []
                self.player_name2 = "Your turn"
                self.footer_message = ''
                self.isTrue2 = True
                self.game_board = None

            async def print_game_board2():
                game_board = (f" {self.a2} | {self.b2} | {self.c2} \n"
                              f" --------- \n"
                              f" {self.d2} | {self.e2} | {self.f2} \n"
                              f" --------- \n"
                              f" {self.g2} | {self.h2} | {self.i2} ")
                embed = disnake.Embed(title="Tic-Tac-Toe")
                embed.add_field(name='', value=f"{game_board}")
                embed.set_footer(text=f"{self.footer_message}")
                if self.game_board is None:
                    pass
                else:
                    await self.game_board.delete()
                self.game_board = await ctx.send(embed=embed)

            async def check_for_winner():
                if len(self.location2) == 0:
                    await ctx.send("It was a tie!")
                    self.isTrue2 = False
                    return False

                for i in self.possible_wins:
                    result = all(i in self.real_player_input_list for i in self.possible_wins[i])
                    if result:
                        await ctx.send(f"You won!")
                        self.isTrue2 = False
                        return False
                for i in self.possible_wins:
                    result = all(i in self.bot_input_list for i in self.possible_wins[i])
                    if result:
                        await ctx.send(f"Bot won!")
                        self.isTrue2 = False
                        return False
                else:
                    self.isTrue2 = True
                    return True

            def remove_from_list(remove_val_from_list):
                if remove_val_from_list in self.location2:
                    self.location2.remove(remove_val_from_list)

            async def bot_location_picker():
                block_user = []
                winning_values = []
                threshold = 2

                # Loop to find possible values to win the game
                for possible_wins_index in self.possible_wins:
                    count = 0
                    for possible_win_values in self.possible_wins[possible_wins_index]:
                        if possible_win_values in self.bot_input_list:
                            count += 1
                    if count >= threshold:
                        for possible_win_values in self.possible_wins[possible_wins_index]:
                            if possible_win_values not in self.bot_input_list:
                                winning_values.append(possible_win_values)
                if winning_values:
                    ran_pick_from_winning_values = random.choice(winning_values)
                    if ran_pick_from_winning_values in self.location2:
                        return ran_pick_from_winning_values

                # Loop to find possible values to block the user from winning the game
                for possible_wins_index in self.possible_wins:
                    count = 0
                    for possible_win_values in self.possible_wins[possible_wins_index]:
                        if possible_win_values in self.real_player_input_list:
                            count += 1
                    if count >= threshold:
                        for possible_win_values in self.possible_wins[possible_wins_index]:
                            if possible_win_values not in self.user1_input_list:
                                block_user.append(possible_win_values)
                # await ctx.send(f"Valid Locations: {self.location2}")
                if not block_user:
                    random_pick = random.choice(self.location2)
                    return random_pick
                else:
                    # await ctx.send(f"Block user locations: {block_user}")
                    block_user = [i for i in block_user if i in self.location2]
                    if not block_user:
                        random_pick = random.choice(self.location2)
                        return random_pick
                    else:
                        ran_pick_from_block_user = random.choice(block_user)
                        return ran_pick_from_block_user

            async def real_player_input():
                def check(msg):
                    return msg.channel == ctx.channel

                while self.isTrue2:
                    try:
                        msg = await self.client.wait_for('message', check=check)
                        if msg.content.casefold() == '-stop':
                            embed = disnake.Embed(title="**Wonky wins**")
                            await ctx.send(embed=embed)
                            self.isTrue2 = False
                            return
                        player_msg_int = int(msg.content)
                        await real_player(player_msg_int)
                        return player_msg_int
                    except ValueError:
                        pass

            async def bot_input():
                bot_picker = await bot_location_picker()
                await bot(bot_picker)
                return bot_picker

            async def real_player(player):
                if player in self.location2:
                    if player == 1:
                        self.a2 = "**X**"
                    elif player == 2:
                        self.b2 = "**X**"
                    elif player == 3:
                        self.c2 = "**X**"
                    elif player == 4:
                        self.d2 = "**X**"
                    elif player == 5:
                        self.e2 = "**X**"
                    elif player == 6:
                        self.f2 = "**X**"
                    elif player == 7:
                        self.g2 = "**X**"
                    elif player == 8:
                        self.h2 = "**X**"
                    elif player == 9:
                        self.i2 = "**X**"

                    remove_val_from_list = player
                    self.real_player_input_list.append(player)
                    remove_from_list(remove_val_from_list)

                    self.player_name2 = ''

                    if not await check_for_winner():
                        return
                else:
                    await ctx.send("\nThat position is already taken, try another position: \n")
                    await real_player_input()

            async def bot(bot_picker):
                if bot_picker in self.location2:
                    if bot_picker == 1:
                        self.a2 = "**O**"
                    elif bot_picker == 2:
                        self.b2 = "**O**"
                    elif bot_picker == 3:
                        self.c2 = "**O**"
                    elif bot_picker == 4:
                        self.d2 = "**O**"
                    elif bot_picker == 5:
                        self.e2 = "**O**"
                    elif bot_picker == 6:
                        self.f2 = "**O**"
                    elif bot_picker == 7:
                        self.g2 = "**O**"
                    elif bot_picker == 8:
                        self.h2 = "**O**"
                    elif bot_picker == 9:
                        self.i2 = "**O**"
                    remove_val_from_list = bot_picker
                    self.bot_input_list.append(bot_picker)
                    remove_from_list(remove_val_from_list)
                    self.footer_message = f"Bot picked: {bot_picker}"

                    if not await check_for_winner():
                        return
                else:
                    await ctx.send(f"Something went wrong")
                    return

            async def user_input():
                while self.isTrue2:

                    await real_player_input()

                    if not self.isTrue2:
                        break

                    await bot_input()
                    await print_game_board2()

                    if not self.isTrue2:
                        break

            '''await ctx.send(f"{self.a2}, {self.b2}, {self.c2}, {self.d2}, {self.e2}, {self.f2}, {self.g2}, {self.h2}, {self.i2}\n"
                           f"{self.location2}\n {self.real_player_input_list}\n {self.bot_input_list}\n {self.player_name2}\n"
                           f" {self.footer_message}\n {self.isTrue2}\n {self.game_board}")'''

            reset_game_values()
            await print_game_board2()
            await user_input()

        except Exception as error:
            error_info = traceback.format_exc()
            print(f"Error: {error}\n{error_info}")
            return


def setup(client):
    client.add_cog(Tic_Tac_Toe(client))
