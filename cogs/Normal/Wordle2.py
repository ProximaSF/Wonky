import asyncio
import random
import disnake
from disnake.ext import commands
from cogs.Normal.random_wordle import RandomWordle


class wordle(commands.Cog):
    wordle_states = {}

    def __init__(self, client):
        self.client = client
        self.ctx = None
        self.message_reactions = {}
        self.hint_reset_interval = 10
        self.message_id = None
        self.old_message_id = None
        self.reacted_users = []
        self.wordle_word = None
        self.hint_displayed = False  # Track if the hint has been displayed
        self.wordle_letters = [] # Store wordle letters to be used for hints
        self.used_letters = [] # Store used letters
        self.used_words = [] # Store used wordle words
        self.letter_contain = []
        self.wordle_letters_stored = False
        self.wordle_reset = False
        self.nitro_giveaway = False
        self.giveaway_msg_send = False  # False to turn off giveaway message and vice versa

    # @commands.has_any_role("Admin")
    @commands.command()
    async def stop_wordle(self, ctx):
        if wordle.wordle_states.get(ctx.guild.id, False):
            wordle.wordle_states[ctx.guild.id] = False
            await ctx.send("**Stopped the wordle command.**")
        else:
            await ctx.send("**No wordle command is currently running.**", delete_after=4)

    @commands.has_any_role("Admin")
    @commands.command()
    async def wordle(self, ctx):
        if wordle.wordle_states.get(ctx.guild.id, False):
            await ctx.send("**Another wordle command is already running.**", delete_after=4)
            return

        wordle.wordle_states[ctx.guild.id] = True

        try:
            while wordle.wordle_states.get(ctx.guild.id, False):

                #grabing the wordle from another file (more complex way)
                rw = RandomWordle(self.client, 'txt/fiveletter.txt')
                self.wordle_word = rw.get_random_wordle()
                print(f"Wordle word: {rw.wordle_word}")


                # alternative way
                '''def get_random_word():
                    with open('cogs/fiveletter.txt', 'r') as f:
                        words = f.read().splitlines()
                    return random.choice(words)

                self.wordle_word = get_random_word()
                print(self.wordle_word)'''

                attempts = random.randint(6, 8)
                chance = random.random()
                bonus_chance = 0.3
                giveaway_chance = 0.1
                #print(chance)


                # Discord nitro giveaway msg

                if not self.nitro_giveaway:
                    if chance < giveaway_chance:
                        attempts = 2
                        # allow giveaway msg to send
                        self.giveaway_msg_send = False

                wordle_info = ("\n---------------------------------------------------------"
                                f"\nGuess the 5 letter word - **{attempts}** attempts."
                                "\n__**Reference**__"
                                "\n1️⃣. **Bold** letter represent correct letter in the correct position."
                                "\n2️⃣. __Underline__ letter represent correct letter but wrong position."
                                "\n3️⃣. ~~Struck-through~~ letters represent the absence of that letter in part of the word."
                                "\n:four:. React to the light bulb to get a hint. `Might need to react again to get hint (IDK why)`."
                                "\n:five:. React to 📜 to get used words & letters."
                                "\n---------------------------------------------------------")

                await asyncio.sleep(1)
                # Giveaway message
                if chance <= giveaway_chance and not self.nitro_giveaway:
                    total_WobbleBits = 100
                    await ctx.send(f"**‼️Solve the word under {attempts} attempts to win __Discord Nitro Basic__ and {total_WobbleBits} WobbleBits‼️** {wordle_info}")
                # Bonus message
                elif chance <= bonus_chance:
                    total_WobbleBits = 100
                    await ctx.send(f"**‼️Earn {total_WobbleBits} WobbleBits regardless which attempt it was guessed on‼️** {wordle_info}")
                # Normal message
                else:
                    total_WobbleBits = 20
                    await ctx.send(f"{wordle_info}")



                '''wordle_characters = []
                for i in range(5):
                    wordle_characters.append(wordle_word[0 + i:1 + i])
                print(wordle_characters)'''
                Entry = 0
                winner = None
                while Entry <= attempts and wordle.wordle_states.get(ctx.guild.id, False):
                    Entry = Entry + 1

                    def check(msg):
                        return msg.channel == ctx.channel

                    def add_WobbleBits(user_id, WobbleBits):
                        user = disnake.utils.get(ctx.guild.members, id=int(user_id))
                        if user.bot:
                            return  # If user is a bot, return without adding WobbleBits

                        with open("txt/playerpoints.txt", "r+", encoding="utf-8") as f:
                            lines = f.readlines()
                            f.seek(0)
                            for i, line in enumerate(lines):
                                if line.startswith(f"[{user_id}]: "):

                                    WobbleBits_line = lines[i + 1]
                                    current_WobbleBits = int(WobbleBits_line.strip().split(': ')[1])
                                    new_WobbleBits = current_WobbleBits + WobbleBits
                                    # print(current_WobbleBits)
                                    lines[i + 1] = f"\tCurrent WobbleBits: {new_WobbleBits}\n"
                                    break
                            f.seek(0)
                            f.writelines(lines)
                            f.truncate()

                    msg = await self.client.wait_for('message', check=check)

                    with open('txt/fiveletter.txt', 'r') as f:
                        words = f.read().splitlines()

                    if msg.content.isalpha():
                        if msg.content.casefold() in self.used_words:
                            Entry = Entry - 1
                            await ctx.send(f"**{msg.content}** already attempted \t{attempts - Entry} attempts")

                        # Giveaway congrats msg
                        elif msg.content.casefold() == self.wordle_word.casefold() and not self.nitro_giveaway and not self.giveaway_msg_send:
                            winner = msg.author.mention
                            # Allow to send DM
                            channel = await ctx.author.create_dm()
                            await ctx.send(f"**Congrats {winner} on solving the word __{self.wordle_word}__**‼️🍾\n Check your DM .")
                            await channel.send(f"**Congrats** again {self.wordle_word}**!\nPlease DM Prox for link and a screenshot of the word you guessed correctly sent by the bot")
                            print(f"**Congrats {winner} on solving the word __{self.wordle_word}__**‼️🍾\n Check your DM .")

                            add_WobbleBits(msg.author.id, total_WobbleBits)
                            self.used_words.clear()
                            self.wordle_letters.clear()
                            self.used_letters.clear()
                            self.letter_contain.clear()
                            self.wordle_letters_stored = False
                            self.nitro_giveaway = True
                            print("Discord giveaway turned off")

                            break
                        elif msg.content.casefold() == self.wordle_word.casefold() and Entry == 1:
                            winner = msg.author.mention
                            await ctx.send(f"{winner} solved the word **{self.wordle_word}** on his/her first attempt!!"
                                            f"\nYou earned {total_WobbleBits}")
                            add_WobbleBits(msg.author.id, total_WobbleBits)
                            self.used_words.clear()
                            self.wordle_letters.clear()
                            self.used_letters.clear()
                            self.letter_contain.clear()
                            self.wordle_letters_stored = False
                            break
                        elif msg.content.casefold() == self.wordle_word.casefold():
                            winner = msg.author.mention
                            if chance <= bonus_chance:
                                await ctx.send(
                                    f"**BONUS:** {winner} solved the word **{self.wordle_word}** on attempt {0 + Entry}!"
                                    f"\nYou earned {total_WobbleBits} WobbleBits!")
                                add_WobbleBits(msg.author.id, total_WobbleBits)
                                self.used_words.clear()
                                self.wordle_letters.clear()
                                self.used_letters.clear()
                                self.letter_contain.clear()
                                self.wordle_letters_stored = False
                                break
                            else:
                                winner = msg.author.mention
                                WobbleBits_awarded = (total_WobbleBits // Entry)
                                await ctx.send(f"{winner} solved the word **{self.wordle_word}** on attempt {0 + Entry}!"
                                                f"\nYou earned {WobbleBits_awarded} WobbleBits!")
                                add_WobbleBits(msg.author.id, WobbleBits_awarded)
                                self.used_words.clear()
                                self.wordle_letters.clear()
                                self.used_letters.clear()
                                self.letter_contain.clear()
                                self.wordle_letters_stored = False
                                break


                        elif len(msg.content) < 5 or len(msg.content) > 5:
                            Entry = Entry - 1
                            await ctx.send(
                                f"Pick a word that have **5** characters/letters.\n**Attempts left: {attempts - Entry}**",
                                delete_after=4)
                            if not msg.author.bot:
                                await msg.delete()

                        elif Entry == attempts:
                            await ctx.send(f"Inputs ran out, the word was **{self.wordle_word}**.")
                            self.used_words.clear()
                            self.wordle_letters.clear()
                            self.used_letters.clear()
                            self.letter_contain.clear()
                            self.wordle_letters_stored = False
                            break
                        elif msg.content.casefold() not in words:
                            Entry = Entry - 1
                            await ctx.send(f"Sorry, that is not a word or it's not in my list, try again."
                                            f"\n**Attempts left: {attempts - Entry}**", delete_after=4)
                            if not msg.author.bot:
                                await msg.delete()
                        else:
                            self.hint_displayed = False
                            capitalized = msg.content
                            self.used_words.append(capitalized)
                            #print(self.used_words)

                            # Store used letters
                            upper_content = msg.content.upper()
                            for letters in upper_content:
                                if letters not in self.used_letters:
                                    self.used_letters.append(letters)
                            self.used_letters.sort()
                            #print(self.used_letters)

                            result = ''
                            for i in range(len(self.wordle_word)):
                                if msg.content.casefold()[i] == self.wordle_word.casefold()[i]:
                                    result += f" **{msg.content.upper()[i]}**"
                                    upper_contain = msg.content.upper()[i]
                                    for letters in upper_contain:
                                        if letters not in self.letter_contain:
                                            self.letter_contain.append(upper_contain)
                                    #print(self.letter_contain)
                                elif msg.content.casefold()[i] in self.wordle_word.casefold():
                                    result += f" __{msg.content.upper()[i]}__"
                                    upper_contain = msg.content.upper()[i]
                                    for letters in upper_contain:
                                        if letters not in self.letter_contain:
                                            self.letter_contain.append(upper_contain)
                                    #print(self.letter_contain)

                                elif msg.content.casefold()[i] not in self.wordle_word.casefold():
                                    result += f" ~~{msg.content.upper()[i]}~~"
                            #print(f"1 {self.reacted_users}")

                            '''Using if self.message_id: is a common practice to check whether there is a previous 
                            message ID stored before attempting to remove a reaction from it'''
                            if self.message_id:
                                # Remove old reaction from the previous message
                                old_message = await ctx.channel.fetch_message(self.message_id)
                                old_emoji = self.client.get_emoji(1198887331990618153)
                                await old_message.remove_reaction(old_emoji, self.client.user)
                                await old_message.remove_reaction('📜', self.client.user)


                            # Send the new message and add a reaction
                            message = await ctx.send(f"{msg.author.name}\t| {result} |\t{attempts - Entry} attempts")
                            self.message_id = message.id
                            emoji = self.client.get_emoji(1198887331990618153)
                            await message.add_reaction(emoji)
                            await message.add_reaction('📜')
                            await msg.delete()

                    else:
                        Entry = Entry - 1
                        if msg.author.bot:
                            continue
                        else:
                            await ctx.send(f"Word must contain **5 letters**, no number or special characters."
                                            f"\n**Attempts left: {attempts - Entry}**", delete_after=4)
                            if not msg.author.bot:
                                await msg.delete()
        finally:
            wordle.wordle_states[ctx.guild.id] = False

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Handle reactions added to messages."""
        # Ignore reactions added by the bot itself
        if user.bot:
            return

        # Hint reaction
        hint_emoji_id = 1198887331990618153
        hint_emoji = self.client.get_emoji(hint_emoji_id)


        if str(reaction.emoji) == '📜' and reaction.message.id == self.message_id:
            embed = disnake.Embed(title=f"", color=disnake.Color.orange())
            embed.add_field(name='**Used words**', value=f'{self.used_words}', inline=False)
            embed.add_field(name='**Used letters**', value=f'{self.used_letters}', inline=False)
            embed.add_field(name='**Letters contain**', value=f'{self.letter_contain}', inline=False)

            await reaction.message.channel.send(embed=embed)
            await reaction.message.remove_reaction(reaction, user)
            await reaction.message.remove_reaction(reaction, reaction.message.guild.me)


        if not self.hint_displayed:
            if reaction.emoji == hint_emoji and reaction.message.id == self.message_id:
                #grab user id when they react
                #self.reacted_users.append(user.id)
                #print(self.reacted_users)

                #print(f"From reaction: Wordle word: {self.wordle_word}")

                size = len(self.wordle_letters)
                if not self.wordle_letters_stored:
                    for i in range(5):
                        self.wordle_letters.append(self.wordle_word[i])
                    self.wordle_letters_stored = True

                else:
                    if size == 1:
                        await reaction.message.channel.send(f"Used up all the hint for this word, the word was **{self.wordle_word}**. New word generated.")
                        self.wordle_reset = True
                    else:
                        random_index = random.choice(range(len(self.wordle_letters)))
                        letter_to_remove = self.wordle_letters[random_index]
                        #print(self.wordle_letters)

                        await reaction.message.channel.send(f"The word contains **{letter_to_remove.upper()}**")
                        self.wordle_letters.pop(random_index)
                        await reaction.message.remove_reaction(reaction, user)
                        await reaction.message.remove_reaction(reaction, reaction.message.guild.me)
                        self.hint_displayed = True

                return

def setup(client):
    client.add_cog(wordle(client))  # bot.add_cog(mech(bot)) is the name of the cog "mech" must match line 8
