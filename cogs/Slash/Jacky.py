import random
import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands

from cogs.System.PointsAdjust import Adjust_WobbleBBits

Instance_WobbleBits = Adjust_WobbleBBits()

class Choice(disnake.ui.View):
    def __init__(self, initiator_id: int):
        super().__init__()
        self.initiator_id = initiator_id
        self.choice = None

    @disnake.ui.button(label="10 Pulls", style=disnake.ButtonStyle.blurple)
    async def choice_a(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.user.id != self.initiator_id:
            await interaction.response.send_message("You are not authorized to interact with this button.",
                                                    ephemeral=True)
            return
        self.choice = button.label
        self.stop()

    @disnake.ui.button(label="One Pull", style=disnake.ButtonStyle.blurple)
    async def choice_b(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.user.id != self.initiator_id:
            await interaction.response.send_message("You are not authorized to interact with this button.",
                                                    ephemeral=True)
            return
        self.choice = button.label
        self.stop()

class Gotcha(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.five_star_threshold = 0.006

    @commands.slash_command(name="bp_gotcha", description="Jacky's Personal Command")
    async def trivia_slash(self, interaction: ApplicationCommandInteraction) -> None:

        jacky_id = 688616729198592001
        prox_id = 246497637963005954
        user_current_wobblebits = int(Instance_WobbleBits.get_WobbleBits(interaction.user.id))

        five_star_threshold_percent = f"{self.five_star_threshold * 100}%"
        four_star_threshold = 0.055
        three_star_threshold = 0.800

        if interaction.user.id != jacky_id and interaction.user.id != prox_id:
            await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
            return

        def random_generator():
            return random.random()

        def ten_pulls():
            if interaction.user.id != prox_id:
                Instance_WobbleBits.sub_WobbleBits(interaction.author.id, 20)

            def ten_pull():
                float_ten_pulls_list = [round(random_generator(), 3) for _ in range(10)]

                name_ten_pulls_list = []
                for i in float_ten_pulls_list:
                    if i <= self.five_star_threshold:
                        name_ten_pulls_list.append("5 star")
                    elif i <= four_star_threshold:
                        name_ten_pulls_list.append("4 star")
                    else:
                        name_ten_pulls_list.append("3 star")

                check_for_4_star_total = sum(
                    1 for value in float_ten_pulls_list if self.five_star_threshold <= value <= four_star_threshold)

                if check_for_4_star_total == 0:
                    name_ten_pulls_list = sorted(name_ten_pulls_list, reverse=True)
                    name_ten_pulls_list.pop(0)
                    name_ten_pulls_list.append("4 star")

                return float_ten_pulls_list, name_ten_pulls_list

            float_ten_pulls_list, name_ten_pulls_list = ten_pull()

            check_for_5_star = any(value <= self.five_star_threshold for value in float_ten_pulls_list)
            check_for_4_star_total = sum(1 for value in float_ten_pulls_list if self.five_star_threshold <= value <= four_star_threshold)
            check_for_3_star_total = 10 - check_for_4_star_total

            name_ten_pulls_list.sort(reverse=True)
            if interaction.user.id == prox_id:
                name_ten_pulls_list.pop(0)
                name_ten_pulls_list.pop(1)
                name_ten_pulls_list.append("5 star")
                name_ten_pulls_list.append("4 star")
                name_ten_pulls_list.sort(reverse=True)
                msg = (f"**There was a 5 star**\n\n"
                       f"**Result:** {float_ten_pulls_list}\n{name_ten_pulls_list}\n"
                       f"**5 Star Rate:** {five_star_threshold_percent} or {self.five_star_threshold}")
            else:
                if check_for_5_star:
                    msg = (f"**There was a 5 star**\n\n"
                           f"**Result:** {float_ten_pulls_list}\n{name_ten_pulls_list}\n"
                           f"**5 Star Rate:** {five_star_threshold_percent} or {self.five_star_threshold}")
                else:
                    def three_star_result_sum(num):
                        sum = 0
                        for i in range(num):
                            result = random.random()
                            if result <= 0.600:
                                sum += 1
                        return sum

                    if check_for_4_star_total == 0:
                        result = 10 + three_star_result_sum(9)
                        Instance_WobbleBits.add_WobbleBits(interaction.author.id, result)
                        msg = (f"**Didn't pull a 5 star**\n\n"
                               f"**Result:** {float_ten_pulls_list}\n{name_ten_pulls_list}\n"
                               f"Gained {result}\n"
                               f"Current Balance: {Instance_WobbleBits.get_WobbleBits(jacky_id)}")
                    else:
                        result = (check_for_4_star_total * 10) + three_star_result_sum(check_for_3_star_total)
                        Instance_WobbleBits.add_WobbleBits(interaction.author.id, result)
                        msg = (f"**Didn't pull a 5 star**\n\n"
                               f"**Result:** {float_ten_pulls_list}\n{name_ten_pulls_list}\n"
                               f"Gained {result}\n"
                               f"Current Balance: {Instance_WobbleBits.get_WobbleBits(jacky_id)}")

            return check_for_5_star, msg

        def single_pull():
            Instance_WobbleBits.sub_WobbleBits(interaction.author.id, 2)
            pull_val = round(random_generator(), 3)
            pull_val_percentage = f"{pull_val * 100}%"
            result = pull_val <= self.five_star_threshold

            def three_star_result():
                return random.randint(0, 1)

            if result:
                msg = (f"**Pulled a 5 star**\n\n"
                       f"**Result:** {pull_val}\n"
                       f"DM Prox")
            else:
                if pull_val <= 0.055:
                    Instance_WobbleBits.add_WobbleBits(interaction.author.id, 10)
                    msg = (f"**Didn't pull a 5 star**\n\n"
                           f"**Result:** {pull_val} or {pull_val_percentage}\n"
                           f"Gained 10 bits. Current balance {Instance_WobbleBits.get_WobbleBits(jacky_id)}")
                else:
                    result = three_star_result()
                    Instance_WobbleBits.add_WobbleBits(interaction.author.id, result)
                    msg = (f"**Didn't pull a 5 star**\n\n"
                           f"**Result:** {pull_val} or {pull_val_percentage}\n"
                           f"Gained {result} bits. Current balance {Instance_WobbleBits.get_WobbleBits(jacky_id)}")
            return result, msg

        buttons = Choice(interaction.user.id)  # Pass the user's ID to the Choice class.

        embed = disnake.Embed(color=disnake.Color.blue())
        embed.add_field(name=f"Pick What Types of Pull You Want", value=f"**Pull Info:**\n"
                                                                        f"20 Bits for 10 pull or 1 for single pulls\n\n"
                                                                        f"**Drop Info:**\n"
                                                                        f"`0.6%` of winning\n"
                                                                        f"`5.5%` of getting 4 star (10 bits)\n"
                                                                        f"`94.3 of getting 3 star (0 or 1 bit)\n")
        embed.set_footer(text=f"You Have {user_current_wobblebits} Wobble Bits\n")
        await interaction.send(embed=embed, view=buttons, ephemeral=False)
        await buttons.wait()  # wait for the user to click a button.

        if buttons.choice == "10 Pulls":
            if user_current_wobblebits < 20:
                embed2 = disnake.Embed(
                    description=f"Don't Have Enough For a 10 pull",
                    color=0xFF9900)
            else:
                ten_pull_bool, ten_pull_msg = ten_pulls()

                if ten_pull_bool:
                    embed2 = disnake.Embed(
                        description=f"{ten_pull_msg}",
                        color=0x00FF00)
                else:
                    embed2 = disnake.Embed(
                        description=f"{ten_pull_msg}",
                        color=0xFF0000)

        else:
            if user_current_wobblebits < 2:
                embed2 = disnake.Embed(
                    description=f"Not Enough Bits to pull",
                    color=0xFF9900)
            else:
                single_pull_bool, single_pull_msg = single_pull()

                if single_pull_bool:
                    embed2 = disnake.Embed(
                        description=f"{single_pull_msg}",
                        color=0x00FF00)
                else:
                    embed2 = disnake.Embed(
                        description=f"{single_pull_msg}",
                        color=0xFF0000)

        await interaction.edit_original_message(embed=embed2, view=None)
        return

def setup(client):
    client.add_cog(Gotcha(client))
