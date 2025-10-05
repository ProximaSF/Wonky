import os
import asyncio
import disnake
import disnake.utils
from disnake.ext import commands
import traceback
import random
#from pillow_simd import Image, ImageDraw (More efficent but cant download)
from PIL import Image, ImageDraw
from io import BytesIO
from PyDictionary import PyDictionary
from cogs.System.Webhook import Webhook
from cogs.System.PointsAdjust import Adjust_WobbleBBits

instance_WobbleBits = Adjust_WobbleBBits()

dictionary = PyDictionary()


class Hangman(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.hangman_word = None
        self.second_empty_word_letters = ''
        self.sorted_word_letter_list = []
        self.attempts = 7
        self.points = 20
        self.word_num_size = 0
        self.upper_msg = None
        self.randomMember = None

        # without this, self.used_letter will not be stored, leading to an empty list
        self.client.add_listener(self.on_reaction_add, 'on_reaction_add')
        self.used_letters = []  # Initialize
        self.message_id = None
        self.message_id2 = None  # To see hangman word meaning after reaction

        self.hint_displayed = False  # Track if the hint has been displayed
        self.hangman_letters_stored = False
        self.hangman_letters = []
        self.hangman_reset = False
        self.add_reaction = True


        self.final_first_empty_word_letters = ''

        self.isTrue = True
        self.isTrue2 = True

    async def hangman(self, ctx):
        # grab a random hangman word (less efficient method)
        # f.read() reads the entire contents of the file into memory as a single string.
        # splitlines() splits the string into a list of lines (words in this case).
        # The resulting list of words is stored in the words variable.
        # random.choice(words) selects a random word from the list and returns it.
        '''def get_random_word():
            with open('txt/hangman_words.txt', 'r') as f:
                words = f.read().splitlines()
            return random.choice(words)'''

        # More efficient method, only grabbing a random word from the line and uses that word
        # instead storing all the words and picking one of them
        def get_random_word():
            with open('txt/hangman_words.txt', 'r') as f:
                lines = f.readlines()
                if lines:
                    return random.choice(lines).strip()
                else:
                    return None

        guild_id = ctx.guild.id
        file_path = f"txt/ServerSettings/{guild_id}/{guild_id}.txt"
        hangman_word = get_random_word()
        all_caps = hangman_word.upper()
        # print(all_caps)

        title = 'Hangman'
        message_description = f'Word: {all_caps}'
        webhook_instance = Webhook()
        webhook_instance.webhook_embed(title, message_description)

        def read_word_game_status():
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    for line in file:
                        if "Word Games:" in line:
                            return line.strip().split(":")[1].strip().lower()

        try:
            def hangman_info():
                self.hangman_word = all_caps
                self.word_num_size = len(self.hangman_word)

                self.randomMember = random.choice(ctx.guild.members)
                # print(self.randomMember)

                for i in range(self.word_num_size):
                    self.sorted_word_letter_list.append(self.hangman_word[i])
                self.sorted_word_letter_list.sort()

            def print_empy_start():
                first_empty_word_letters = ''
                for _ in range(self.word_num_size):
                    first_empty_word_letters += "• "  # Underscore will not work cuz its used for txt formating in discord.
                self.final_first_empty_word_letters = first_empty_word_letters
                return first_empty_word_letters.strip(' ')

            async def check_input():
                correct_letters = []
                def check(msg):
                    return msg.channel == ctx.channel

                while self.isTrue2:
                    if read_word_game_status() == "false":
                        break
                    msg = await self.client.wait_for('message', check=check)
                    self.upper_msg = msg.content.upper()

                    if msg.content.casefold() == "-stop":
                        await asyncio.sleep(0.5)
                        embed = disnake.Embed(title=f'**Hangman skipped**')
                        embed.add_field(name='', value=f"Word was: **{self.hangman_word}**")
                        message = await ctx.send(embed=embed)
                        self.message_id2 = message.id
                        await message.add_reaction('❓')
                        self.isTrue2 = False
                        return

                    elif not msg.content.isalpha() or len(msg.content) > 1:
                        if msg.author.bot:
                            continue
                        else:
                            pass
                            #await ctx.send("Only enter 1 letter", delete_after=4)

                    else:

                        if self.upper_msg in self.used_letters:
                            await asyncio.sleep(0.5)
                            embed = disnake.Embed(title=f'Already used **{self.upper_msg}**')
                            embed.set_footer(text=f"Attempts left: {self.attempts - 1}")
                            await ctx.send(embed=embed, delete_after=4)

                            #await ctx.send(f"Used letter: {self.used_letters}")
                            #await ctx.send(f"Correct letter: {correct_letters}")

                        elif not self.upper_msg in self.hangman_word:
                            self.used_letters.append(self.upper_msg)

                            self.attempts -= 1
                            self.points -= 2
                            await asyncio.sleep(0.5)
                            msg_author = msg.author.id
                            await draw_hangman(msg_author)

                        elif self.upper_msg in self.hangman_word:
                            self.used_letters.append(self.upper_msg)

                            # Add the correct number of valid letters in the correct_letter list to be compare with
                            count = self.sorted_word_letter_list.count(self.upper_msg)

                            # print(count)
                            for i in range(0, count):
                                correct_letters.append(self.upper_msg)
                            correct_letters.sort()

                            used_letters_2 = []
                            final_list = {}
                            for i in range(self.word_num_size):
                                pos = []
                                letter = self.hangman_word[i]
                                if letter in used_letters_2:
                                    continue
                                else:
                                    used_letters_2.append(letter)
                                    for j in range(self.word_num_size):
                                        if letter == self.hangman_word[j]:
                                            pos.append(j)
                                    final_list[letter] = pos
                            # await ctx.send(final_list)
                            pos_letter_dic = final_list[self.upper_msg]

                            if correct_letters == self.sorted_word_letter_list:
                                winner = msg.author.mention
                                message = await ctx.send(f"{winner} solved the word **{self.hangman_word}**, you earned **{self.points}** points!")
                                instance_WobbleBits.add_WobbleBits(msg.author.id, self.points)
                                self.isTrue2 = False
                                self.message_id2 = message.id
                                await message.add_reaction('❓')

                                # await ctx.send(correct_letters)
                                # await ctx.send(self.sorted_word_letter_list)
                            else:
                                await change(pos_letter_dic)

            async def change(pos_letter_dic):
                if self.isTrue:
                    for _ in range(self.word_num_size):
                        self.second_empty_word_letters += "•"
                    self.isTrue = False

                word_letters_list = list(self.second_empty_word_letters)

                for i in range(self.word_num_size):
                    if i in pos_letter_dic:
                        word_letters_list[i] = self.upper_msg
                self.second_empty_word_letters = ''.join(word_letters_list)

                word_letters_final_list = list(self.second_empty_word_letters)
                # print(word_letters_final_list)
                word_letters_final_list_size = len(word_letters_final_list) + (len(word_letters_final_list) - 1)

                for i in range(word_letters_final_list_size):
                    if i % 2 != 0:
                        word_letters_final_list.insert(i, ' ')
                show_result = ''.join(word_letters_final_list)
                self.final_first_empty_word_letters = show_result
                await asyncio.sleep(0.5)
                embed = disnake.Embed(title=f'{show_result}')
                embed.set_footer(text=f"Attempts: {self.attempts - 1}")
                message = await ctx.send(embed=embed)

                async def remove_old_reactions(old_message):
                    old_emoji = self.client.get_emoji(1198887331990618153)
                    await old_message.remove_reaction(old_emoji, self.client.user)
                    await old_message.remove_reaction('📜', self.client.user)

                if self.message_id:
                    old_message = await ctx.channel.fetch_message(self.message_id)
                    await remove_old_reactions(old_message)

                async def add_new_reactions(message):
                    emoji = self.client.get_emoji(1198887331990618153)
                    await message.add_reaction(emoji)
                    await message.add_reaction('📜')

                self.message_id = message.id
                await asyncio.gather(add_new_reactions(message))

            async def display_hangman_head():
                user = self.randomMember
                empty_hangman_image = Image.open("images/hangman/hangman_empty.png")

                data = BytesIO(await user.display_avatar.read())
                pfp = Image.open(data)

                pfp = pfp.resize((200, 200))

                # Create a new image with same size as the pfp for the mask
                mask = Image.new('L', pfp.size, 0)
                mask_draw = ImageDraw.Draw(mask)

                # Draw a white circle on the mask
                mask_draw.ellipse((0, 0) + pfp.size, fill=255)

                # Create a new image with transparency and paste the pfp onto it using the mask
                result = Image.new('RGBA', pfp.size)
                result.paste(pfp, mask=mask)

                # Apply the mask to the pfp
                pfp.putalpha(mask)

                # Pos of the image
                empty_hangman_image.paste(result, (430, 290), result)
                empty_hangman_image.save("images/hangman/changes/hangman_head.png")
            async def display_hangman_body():
                user = self.randomMember
                empty_hangman_image = Image.open("images/hangman/hangman_body.png")
                data = BytesIO(await user.display_avatar.read())
                pfp = Image.open(data)
                pfp = pfp.resize((200, 200))
                mask = Image.new('L', pfp.size, 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse((0, 0) + pfp.size, fill=255)
                result = Image.new('RGBA', pfp.size)
                result.paste(pfp, mask=mask)
                pfp.putalpha(mask)
                empty_hangman_image.paste(result, (430, 290), result)
                empty_hangman_image.save("images/hangman/changes/hangman_body.png")
            async def display_hangman_left_arm():
                user = self.randomMember
                empty_hangman_image = Image.open("images/hangman/hangman_arm_left.png")
                data = BytesIO(await user.display_avatar.read())
                pfp = Image.open(data)
                pfp = pfp.resize((200, 200))
                mask = Image.new('L', pfp.size, 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse((0, 0) + pfp.size, fill=255)
                result = Image.new('RGBA', pfp.size)
                result.paste(pfp, mask=mask)
                pfp.putalpha(mask)
                empty_hangman_image.paste(result, (430, 290), result)
                empty_hangman_image.save("images/hangman/changes/hangman_arm_left.png")
            async def display_hangman_right_arm():
                user = self.randomMember
                empty_hangman_image = Image.open("images/hangman/hangman_arm_right.png")
                data = BytesIO(await user.display_avatar.read())
                pfp = Image.open(data)
                pfp = pfp.resize((200, 200))
                mask = Image.new('L', pfp.size, 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse((0, 0) + pfp.size, fill=255)
                result = Image.new('RGBA', pfp.size)
                result.paste(pfp, mask=mask)
                pfp.putalpha(mask)
                empty_hangman_image.paste(result, (430, 290), result)
                empty_hangman_image.save("images/hangman/changes/hangman_arm_right.png")
            async def display_hangman_left_leg():
                user = self.randomMember
                empty_hangman_image = Image.open("images/hangman/hangman_leg_left.png")
                data = BytesIO(await user.display_avatar.read())
                pfp = Image.open(data)
                pfp = pfp.resize((200, 200))
                mask = Image.new('L', pfp.size, 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse((0, 0) + pfp.size, fill=255)
                result = Image.new('RGBA', pfp.size)
                result.paste(pfp, mask=mask)
                pfp.putalpha(mask)
                empty_hangman_image.paste(result, (430, 290), result)
                empty_hangman_image.save("images/hangman/changes/hangman_leg_left.png")
            async def display_hangman_right_leg():
                user = self.randomMember
                empty_hangman_image = Image.open("images/hangman/hangman_leg_right.png")
                data = BytesIO(await user.display_avatar.read())
                pfp = Image.open(data)
                pfp = pfp.resize((200, 200))
                mask = Image.new('L', pfp.size, 0)
                mask_draw = ImageDraw.Draw(mask)
                mask_draw.ellipse((0, 0) + pfp.size, fill=255)
                result = Image.new('RGBA', pfp.size)
                result.paste(pfp, mask=mask)
                pfp.putalpha(mask)
                empty_hangman_image.paste(result, (430, 290), result)
                empty_hangman_image.save("images/hangman/changes/hangman_leg_right.png")

            async def draw_hangman(msg_author):
                await display_hangman_head()
                await display_hangman_body()
                await display_hangman_left_arm()
                await display_hangman_right_arm()
                await display_hangman_left_leg()
                await display_hangman_right_leg()

                body_parts = {
                    6: ['images/hangman/changes/hangman_head.png', 'hangman_head.png'],
                    5: ['images/hangman/changes/hangman_body.png', 'hangman_body.png'],
                    4: ['images/hangman/changes/hangman_arm_left.png', 'hangman_arm_left.png'],
                    3: ['images/hangman/changes/hangman_arm_right.png', 'hangman_arm_right.png'],
                    2: ['images/hangman/changes/hangman_leg_left.png', 'hangman_leg_left.png'],
                    1: ['images/hangman/changes/hangman_leg_right.png', 'hangman_leg_right.png']
                }

                if self.attempts != 1:
                    f = disnake.File(body_parts[self.attempts][0], filename=body_parts[self.attempts][1])
                    embed = disnake.Embed(title=f'**{self.upper_msg}** is not part of the word')
                    embed.add_field(name=f'{self.final_first_empty_word_letters}', value='')
                    embed.set_image(url=f"attachment://{body_parts[self.attempts][1]}")
                    embed.set_footer(text=f"Attempts left: {self.attempts - 1}")
                    message = await ctx.send(file=f, embed=embed)

                    async def remove_old_reactions(old_message):
                        old_emoji = self.client.get_emoji(1198887331990618153)
                        await old_message.remove_reaction(old_emoji, self.client.user)
                        await old_message.remove_reaction('📜', self.client.user)

                    if self.message_id:
                        old_message = await ctx.channel.fetch_message(self.message_id)
                        await remove_old_reactions(old_message)

                    async def add_new_reactions(message):
                        emoji = self.client.get_emoji(1198887331990618153)
                        await message.add_reaction(emoji)
                        await message.add_reaction('📜')

                    self.message_id = message.id
                    await asyncio.gather(add_new_reactions(message))

                else:
                    f = disnake.File(body_parts[self.attempts][0], filename=body_parts[self.attempts][1])
                    embed = disnake.Embed(title=f'Ran out of attempts')
                    embed.add_field(name='', value=f'The word was **{self.hangman_word}**')
                    embed.set_image(url=f"attachment://{body_parts[self.attempts][1]}")
                    embed.set_footer(text=f"Attempts left: {self.attempts - 1}")
                    await ctx.send(file=f, embed=embed)
                    self.isTrue2 = False
                    instance_WobbleBits.add_WobbleBits(msg_author, 5)
                    #await ctx.send(body_parts[self.attempts])


            async def start_msg():
                hangman_info()
                Hangman_info = (
                    f":regional_indicator_h:  :regional_indicator_a:  :regional_indicator_n:  :regional_indicator_g:  :regional_indicator_m:  :regional_indicator_a:  :regional_indicator_n:"
                    "\n---------------------------------------------------------"
                    f"\n**{self.randomMember}** was selected - **{self.attempts - 1}** attempts."
                    "\n1️⃣. Wait for 1s after entering a letter."
                    "\n2️⃣. React to the light bulb to get a hint. `Might need to react again to get hint (IDKW)`."
                    "\n:four:. React 📜 to see used letter(s)."
                    f'\nSize of the word: **{self.word_num_size}**'
                    f'\n**{print_empy_start()}**'
                    "\n---------------------------------------------------------")
                await ctx.send(f"{Hangman_info}")
                await asyncio.sleep(0.5)
                await check_input()
            await start_msg()

        except Exception as error:
            error_info = traceback.format_exc()
            await ctx.send(f"Error: {error}")
            print(f"Error: {error}\n{error_info}")
            return

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

        if str(reaction.emoji) == '❓' and reaction.message.id == self.message_id2:
            try:
                # print("Reaction detected")
                meaning = dictionary.meaning(self.hangman_word)
                meaning_msg = ""

                for i in meaning:
                    content = i
                    meaning_msg += f"**{content}**\n"

                    for j in range(0, len(meaning[i])):
                        meaning_msg += f"{j + 1}. {meaning[content][j].capitalize()}\n"

                embed = disnake.Embed(title=f"", color=disnake.Color.orange())
                embed.add_field(name=f'**{self.hangman_word.upper()} Meaning:**', value=f'', inline=False)
                embed.add_field(name='', value=f'{meaning_msg}', inline=False)

                await reaction.message.channel.send(embed=embed)
                await reaction.message.remove_reaction(reaction, member)
                await reaction.message.remove_reaction(reaction, reaction.message.guild.me)
            except Exception as error:
                pass

        if str(reaction.emoji) == '📜' and reaction.message.id == self.message_id:
            embed = disnake.Embed(title=f"")
            embed.add_field(name='**Letters Used**', value=f'{self.used_letters}', inline=False)
            await reaction.message.channel.send(embed=embed)
            await reaction.message.remove_reaction(reaction, member)
            await reaction.message.remove_reaction(reaction, reaction.message.guild.me)

        if not self.hint_displayed:
            if reaction.emoji == hint_emoji and reaction.message.id == self.message_id:
                # grab user id when they react
                # self.reacted_users.append(user.id)
                # print(self.reacted_users)

                # print(f"From reaction: Wordle word: {self.wordle_word}")


                if not self.hangman_letters_stored:
                    for i in range(5):
                        self.hangman_letters.append(self.hangman_word[i])
                    self.hangman_letters_stored = True

                else:
                    if self.word_num_size == 1:
                        await reaction.message.channel.send(
                            f"Used up all the hint for this word, the word was **{self.hangman_word}**. New word generated.")
                        self.hangman_reset = True
                    else:
                        random_index = random.choice(range(len(self.hangman_letters)))
                        letter_to_remove = self.hangman_letters[random_index]
                        # print(self.wordle_letters)

                        await reaction.message.channel.send(f"The word contains **{letter_to_remove.upper()}**")
                        self.hangman_letters.pop(random_index)
                        await reaction.message.remove_reaction(reaction, user)
                        await reaction.message.remove_reaction(reaction, reaction.message.guild.me)
                        self.hint_displayed = True
                return



def setup(client):
    client.add_cog(Hangman(client))  # bot.add_cog(mech(bot)) is the name of the cog "mech" must match line 8