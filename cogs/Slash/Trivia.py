import random
import json
from urllib.request import urlopen
import disnake
from disnake import ApplicationCommandInteraction
from disnake.ext import commands
from cogs.System.Webhook import Webhook
from cogs.System.PointsAdjust import Adjust_WobbleBBits
instance_WobbleBits = Adjust_WobbleBBits()

class Choice(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.choice = None

    @disnake.ui.button(label="A", style=disnake.ButtonStyle.blurple)
    async def choice_a(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.upper()
        self.stop()

    @disnake.ui.button(label="B", style=disnake.ButtonStyle.blurple)
    async def choice_b(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.upper()
        self.stop()

    @disnake.ui.button(label="C", style=disnake.ButtonStyle.blurple)
    async def choice_c(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.upper()
        self.stop()

    @disnake.ui.button(label="D", style=disnake.ButtonStyle.blurple)
    async def choice_d(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        self.choice = button.label.upper()
        self.stop()

class Trivia_Slash(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.url = 'https://opentdb.com/api.php?amount=1&type=multiple'

    def trivia(self):
        response = urlopen(self.url)
        data_json = json.load(response)
        trivia_msg = ''
        choices = []
        for result in data_json.get("results", []):
            for key, value in result.items():
                if key == "correct_answer":
                    correct_answer = value.replace("&quot;", "\"").replace("&#039;", "'")
                    choices.append(correct_answer)
                elif key == "incorrect_answers":
                    for index, string in enumerate(value):
                        incorrect_answers = string.replace("&quot;", "\"").replace("&#039;", "'")
                        choices.append(incorrect_answers)
                elif key == "question":
                    question = value.replace("&quot;", "\"").replace("&#039;", "'")
                elif key == "category":
                    category = value.replace("&amp;", "&")
                else:
                    trivia_msg += f"{key}: {value}\n"

            random.shuffle(choices)
            choices_dic = {}
            keys = ["A", "B", "C", "D"]
            for i in range(len(choices)):
                choices_dic[keys[i]] = choices[i]

            choice_msg = ""
            for choice_key, choice_val in choices_dic.items():
                choice_msg += f"**{choice_key}**. **{choice_val}**\n"

            difficulty = result.get("difficulty")
            correct_answer = result.get("correct_answer")

            title = "Trivia"
            message_description = f'Answer: {correct_answer}'
            webhook_instance = Webhook()
            webhook_instance.webhook_embed(title, message_description)

            return question, choice_msg, category, difficulty, correct_answer, choices_dic

    @commands.slash_command(name="trivia", description="A random trivia question")
    async def trivia_slash(self, interaction: ApplicationCommandInteraction) -> None:
        buttons = Choice()  # Create an instance of our Choice class.
        question, choice_msg, category, difficulty, correct_answer, choices_dic = self.trivia()  # Get trivia info.

        embed = disnake.Embed(color=disnake.Color.blue())
        embed.add_field(name=f"\n{question}:", value=f"---------------"
                                                     f"\n"
                                                     f"{choice_msg}")
        embed.set_footer(text=f"{category} ({difficulty.upper()})")
        await interaction.send(embed=embed, view=buttons)
        await buttons.wait()  # We wait for the user to click a button.

        user_user = interaction.user
        # print(user_user)

        # await interaction.send(f"TEST1")
        # print(choices_dic)
        # print(f"{buttons.choice}: {correct_answer}")
        if choices_dic[buttons.choice] == correct_answer:
            instance_WobbleBits.add_WobbleBits(interaction.author.id, 2)
            msg = "Correct"
            # User guessed correctly
            embed2 = disnake.Embed(
                description=f"Correct! You guessed `{buttons.choice}`",
                color=0x9C84EF
            )
        else:
            msg = f"Incorrect, it was **{correct_answer}**"
            embed2 = disnake.Embed(
                description=f"Incorrect, it was **{correct_answer}**",
                color=0xE02B2B
            )
        # await interaction.send("TEST2") # Reply to the embed for some reason
        await interaction.channel.send(f"{msg}")    # Send out a normal msg
        await interaction.edit_original_message(embed=embed, view=None)
        return

def setup(client):
    client.add_cog(Trivia_Slash(client))