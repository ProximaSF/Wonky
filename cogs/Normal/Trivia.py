import random
import json
from urllib.request import urlopen
import disnake
from disnake.ext import commands
from cogs.System.Webhook import Webhook
from cogs.System.PointsAdjust import Adjust_WobbleBBits

instance_WobbleBits = Adjust_WobbleBBits()
class Choice(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=10000000000000)
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

class Trivia(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.url = 'https://opentdb.com/api.php?amount=1&type=multiple'

    def trivia(self):
        response = urlopen(self.url)
        data_json = json.load(response)
        trivia_msg = ''
        choices = []

        # The get() method is used to retrieve the value associated with a specified key from a dictionary.
        # The [] set the value to an empty list if the key does not exist, use to prevent a keyError
        for result in data_json.get("results", []):
            for key, value in result.items():
                if key == "correct_answer":
                    correct_answer = value.replace("&quot;", "\"").replace("&#039;", "'") # You can chain the replace method
                    choices.append(correct_answer)
                elif key == "incorrect_answers":
                    # The enumerate method count the number of index based on a given iterable data type (list, string, ...)
                    # The default count index is zero if not given after the iterable type ("value" in this case)
                    # It create a tuple with the index and the value.
                    # For a list letters = ['a', 'b', 'c'] -> list(enumerate(letters)) -> [(0, 'a'), (1, 'b'), (2, 'c')]
                    # For a string word = "cool" -> list(enumerate(word, 2)) -> [(2, 'c'), (3, '0'), (4, 'o'), (5, 'l')]
                    for index, string in enumerate(value):
                        incorrect_answers = string.replace("&quot;", "\"").replace("&#039;", "'")
                        choices.append(incorrect_answers)
                elif key == "question":
                    question = value.replace("&quot;", "\"").replace("&#039;", "'")
                elif key == "category":
                    category = value.replace("&amp;", "&")
                else:
                    trivia_msg += f"{key}: {value}\n"

            # Use the shuffle method from the random package to shuffle items in a list.
            # It will affect the original list.
            random.shuffle(choices)
            choices_dic = {}
            keys = ["A", "B", "C", "D"]
            for i in range(len(choices)):
                # Fill the choices_dic with keys assigned to a values based on the index of the shuffled list.
                choices_dic[keys[i]] = choices[i]
            choice_msg = ""
            # Create list of tuples with each tuples have its corresponding key and values based on the dictionary
            # choice_msg dict_items([("A": ...), ("B": ..., ...), ... ])
            for choice_key, choice_val in choices_dic.items():
                choice_msg += f"**{choice_key}**. **{choice_val}**\n"

            difficulty = result.get("difficulty")
            correct_answer = result.get("correct_answer")

            # Send answer to webhook
            title = "Trivia"
            message_description = f'Answer: {correct_answer}'
            webhook_instance = Webhook()
            webhook_instance.webhook_embed(title, message_description)

            return question, choice_msg, category, difficulty, correct_answer, choices_dic

    @commands.command()
    async def tri(self, ctx) -> None:
        try:
            buttons = Choice()  # Create an instance of our Choice class.
            question, choice_msg, category, difficulty, correct_answer, choices_dic = self.trivia()  # Get trivia info.

            embed = disnake.Embed(color=disnake.Color.blue())
            embed.add_field(name=f"\n{question}", value=f"---------------"
                                                         f"\n"
                                                         f"{choice_msg}")
            embed.set_footer(text=f"{category} ({difficulty.upper()})")
            message = await ctx.send(embed=embed, view=buttons)
            await buttons.wait()    # We wait for the user to click a button.

            user_user = ctx.author
            # print(user_user)

            if choices_dic[buttons.choice] == correct_answer:
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
            await ctx.send(f"{msg}")    # Send out a normal msg
            await message.edit(embed=embed, view=None)
            return
        except Exception as e:
            print(e)


    async def trivia_auto(self, ctx) -> None:
        try:
            buttons = Choice()  # Create an instance of our Choice class.
            question, choice_msg, category, difficulty, correct_answer, choices_dic = self.trivia()  # Get trivia info.

            embed = disnake.Embed(color=disnake.Color.blue())
            embed.add_field(name=f"\n{question}", value=f"---------------"
                                                         f"\n"
                                                         f"{choice_msg}")
            embed.set_footer(text=f"{category} ({difficulty.upper()})")
            message = await ctx.send(embed=embed, view=buttons)
            await buttons.wait()    # We wait for the user to click a button.

            user_user = ctx.author
            # print(user_user)

            value = correct_answer
            # Get the key for the correct answer value from choices_dic
            key = [k for k, v in choices_dic.items() if v == value]
            if choices_dic[buttons.choice] == correct_answer:
                instance_WobbleBits.add_WobbleBits(ctx.author.id, 4)
                msg = f"Correct! It was **{buttons.choice}**, earned 4 bits!"
                # User guessed correctly
                embed2 = disnake.Embed(
                    description=f"Correct! It was `{buttons.choice}`",
                    color=0x9C84EF
                )
            else:
                msg = f"Incorrect, it was **{key[0]}**"
                embed2 = disnake.Embed(
                    description=f"Incorrect, it was **{correct_answer}**",
                    color=0xE02B2B
                )
            # await interaction.send("TEST2") # Reply to the embed for some reason
            await message.reply(f"{msg}")    # Send out a normal msg
            await message.edit(embed=embed, view=None)
            return
        except Exception as e:
            print(e)

def setup(client):
    client.add_cog(Trivia(client))