import asyncio
from disnake.ext import commands

def add_word_count(word):
    with open("txt/WordCounter/WordCounter.txt", "r+") as f:
        lines = f.readlines()
        f.seek(0)
        for i, line in enumerate(lines):
            if word.casefold() in line.casefold():
                current_word_count = int(line.strip().split(': ')[1])
                new_word_count = current_word_count + 1
                lines[i] = f"{word}: {new_word_count}\n"
        f.seek(0)
        f.writelines(lines)
        f.truncate()


def extract_word():
    with open('txt/WordCounter/WordCounter.txt', 'r') as f:
        lines = f.readlines()
        words = [line.split(':')[0].strip() for line in lines]
        return words


class WordCounter(commands.Cog):
    def __init__(self, client):
        self.author = None
        self.word_count = None
        self.last_item = None
        self.client = client
        self.found_words = {}  # Initialize an empty dictionary to store found words and their counts

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.client.user:
            return

        message_content = msg.content

        # Initialize a dictionary to store found words and their counts for this message
        message_found_words = {}

        for word in extract_word():
            singular_word = word.casefold()
            plural_word = singular_word + 's'

            singular_count = message_content.casefold().count(singular_word)
            plural_count = message_content.casefold().count(plural_word)

            if singular_count > 0 or plural_count > 0:
                message_found_words[word] = (singular_count, plural_count)

        if message_found_words:
            sender = msg.author.mention
            #await msg.reply(f"{sender} mentioned the following words: {', '.join(message_found_words.keys())}")

            # Update the counts in the self.found_words dictionary
            for word, (singular_count, plural_count) in message_found_words.items():
                if word in self.found_words:
                    self.found_words[word][0] += singular_count
                    self.found_words[word][1] += plural_count
                else:
                    self.found_words[word] = [singular_count, plural_count]

            # Call add_word_count for each found word to update the counts in the file
            for word, (singular_count, plural_count) in message_found_words.items():
                if singular_count > 0:
                    add_word_count(word)
                if plural_count > 0:
                    add_word_count(word + 's')  # Add plural form separately

        # Now self.found_words contains the counts for all found words in the current message

    @commands.command()
    async def wordc(self, ctx, arg):
        def extract_count(word):
            with open("txt/WordCounter/WordCounter.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    if word.casefold() in line.casefold():
                        return int(line.strip().split(': ')[1])
            return 0

        word_to_check = arg.casefold()
        await asyncio.sleep(1)

        count = extract_count(word_to_check)

        if count > 0:
            await ctx.send(f"The word '{word_to_check}' has been used {count} times.")
        else:
            await ctx.send(f"The word '{word_to_check}' has not been found.")

    @commands.command()
    async def listwords(self, ctx):
        word_list = extract_word()
        if word_list:
            word_list_str = "\n".join(word_list)
            await ctx.send(f"List of words in the text file:\n```\n{word_list_str}\n```")
        else:
            await ctx.send("The text file is empty, and there are no words to list.")

    @commands.command() # will call the last item in the list in the file playerpoint.txt so addlast can be used
    async def getLword(self, ctx):
        global last_item
        with open("txt/WordCounter/WordCounter.txt", 'r') as f:
            lines = f.readlines()

        for line in lines:
            if ":" in line:
                last_item = line.split(":")[0].strip()  # update last_item if a new item is found
            elif '[' in line and ']' in line:
                pass  # reset last_item when a new user is found
            else:
                continue  # ignore other lines
        await ctx.send(f"Last item is **{last_item}**")
        self.last_item = last_item
    @commands.command()  # can be used once last2402 has been used
    async def addword(self, ctx):

        editing_timer = 10
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        if self.last_item is None:
            await ctx.send(f"Use **getLword** first to get the last word in the list")
            return

        await ctx.send(f"What item do you want to add at the end of the list? You have 10s to respond.")

        try:
            msg = await self.client.wait_for('message', check=check, timeout=editing_timer)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond, try the command again.")
            self.last_item = None

        if len(msg.content.split()) != 1:
            await ctx.send("Please enter a single word next time. Use **getLword** again.")
            self.last_item = None
            return

        singular_word = msg.content.strip().casefold()
        plural_word = None

        with open("txt/WordCounter/WordCounter.txt", 'r') as f:
            lines = f.readlines()

        # Check if the word is already in the file
        for line in lines:
            if singular_word in line.casefold():
                await ctx.send(f"The word '{singular_word}' is already in the list. Use **getLword** again.")
                self.last_item = None
                return


        # Ask if they want to add the plural form
        await ctx.send(f"Do you want to add the plural form of '{singular_word}' as well? (yes/no)")

        try:
            response = await self.client.wait_for('message', check=check, timeout=editing_timer)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond, singular form added only.")
        else:
            if response.content.lower() == 'yes':
                # Generate the plural form (you might want to improve this)
                plural_word = singular_word + 's'


        with open("txt/WordCounter/WordCounter.txt", 'w') as f:
            for line in lines:
                if self.last_item in line:
                    line = line.rstrip('\n') + f"\n{singular_word}: 0\n"
                    if plural_word:
                        line += f"{plural_word}: 0\n"
                f.write(line)

            if plural_word:
                await ctx.send(
                    f"'{singular_word}' and its plural form '{plural_word}' have been added. Use **getLword** again to reuse this command.")
            else:
                await ctx.send(f"'{singular_word}' has been added. Use **getLword** again to reuse this command.")
            self.last_item = None
def setup(client):
    client.add_cog(WordCounter(client))