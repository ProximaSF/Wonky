import disnake
from disnake.ext import commands
from disnake import Interaction
from disnake import FFmpegPCMAudio
from disnake import Member

import asyncio
import random
import re
import giphy_client
from giphy_client.rest import ApiException



class meh(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def guess(self, ctx):
        try:
            await ctx.send(f"Pick a range of numbers you want and the number of attempts you want."
                           f"Ex: '__**1-10**, **4**__' or '__**600-10**, **200**__'")

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            msg = await self.client.wait_for('message', check=check)

            user_range = msg.content
            num = re.findall(r'\d+', user_range)  # get the values from the msg.content or user input
            range_1 = int(num[0])
            range_2 = int(num[1])
            attempt = int(num[2])

            if range_1 > range_2:
                range_1 = int(num[1])
                range_2 = int(num[0])
                await ctx.send(
                    f"Now guess a number between **{range_1}-{range_2}**, you have **{attempt}** attempts. Type 'stop' to give up.")

                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel

                Entry = 0
                ran_picker = random.randrange(range_1, range_2)
                while Entry <= attempt:
                    msg = await self.client.wait_for('message', check=check)
                    Entry = Entry + 1
                    if msg.content == "stop" or msg.content == "Stop":
                        await ctx.send(f"You gave up 😢")
                        await ctx.send(f"The number was **{ran_picker}**")
                        break
                    elif int(msg.content) == ran_picker:
                        await ctx.send(f"**Good job, it was {ran_picker}!**")
                        break
                    elif int(msg.content) > range_2 or int(msg.content) < range_1:
                        await ctx.send(f"Pick a number between **{range_1}-{range_2}**!")
                        Entry = Entry - 1
                        print(Entry)
                    elif Entry == attempt:
                        await ctx.send(f"You ran out of inputs, it was **{ran_picker}**!")
                        break
                    else:
                        await ctx.send(f"Nope, keep guessing", delete_after=2)
            else:
                await ctx.send(
                    f"Now guess a number between **{range_1}-{range_2}**, you have **{attempt}** attempts. Type 'stop' to give up.")

                def check(msg):
                    return msg.author == ctx.author and msg.channel == ctx.channel

                Entry = 0
                ran_picker = random.randrange(range_1, range_2)
                while Entry <= attempt:
                    msg = await self.client.wait_for('message', check=check)
                    Entry = Entry + 1
                    if msg.content == "stop" or msg.content == "Stop":
                        await ctx.send(f"You gave up 😢")
                        await ctx.send(f"The number was **{ran_picker}**")
                        break
                    elif int(msg.content) == ran_picker:
                        await ctx.send(f"**Good job, it was {ran_picker}!**")
                        break
                    elif int(msg.content) > range_2 or int(msg.content) < range_1:
                        await ctx.send(f"Pick a number between **{range_1}-{range_2}**!")
                        Entry = Entry - 1
                        print(Entry)
                    elif Entry == attempt:
                        await ctx.send(f"You ran out of inputs, it was **{ran_picker}**!")
                        break
                    else:
                        await ctx.send(f"Nope, keep guessing", delete_after=2)
        except Exception as error:
            print(f"{error}")
            await ctx.send(f"Problem: **[{error}]**")

    @commands.command()
    async def guess02(self, ctx):
        try:
            await ctx.send(f"Guess a number between 1-10. Type 'stop' to end the guess")

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            Entry = 0
            ran_picker = random.randrange(1, 10)
            while Entry <= 3:


                msg = await self.client.wait_for('message', check=check)
                Entry = Entry + 1
                if msg.content == "stop" or msg.content == "Stop":
                    await ctx.send(f"You gave up 😢")
                    await ctx.send(f"The number was **{ran_picker}**")
                    break
                elif int(msg.content) == ran_picker:
                    await ctx.send(f"**Good job, it was {ran_picker}!**")
                    break
                elif int(msg.content) > 10 or int(msg.content) < 1:
                    await ctx.send(f"Pick a number between **1-10**!")
                    Entry = Entry - 1
                    print(Entry)
                elif Entry == 3:
                    await ctx.send(f"You ran out of inputs, it was **{ran_picker}**!")
                    break
                else:
                    await ctx.send(f"Nope, keep guessing", delete_after=2)
        except Exception as error:
            print(f"{error}")
            await ctx.send(f"Problem: **[{error}]**")

    @commands.command()
    async def gif(self, ctx, *, q="smile"):
        api_key = "lPOzaKdQZOQ70qV7vEonJO4tL017bvbK"
        api_instance = giphy_client.DefaultApi()

        try:
            api_response = api_instance.gifs_search_get(api_key, q, limit=20, rating='g')
            lst = list(api_response.data)
            giff = random.choice(lst)

            await ctx.send(giff.embed_url)
            print(giff.embed_url)

        except ApiException as e:
            print("Exception when called Api")

    @commands.command()
    async def useless_info(self, ctx):
        await asyncio.sleep(0.5)
        info = ["No number from 1 to 999 includes the letter 'a' in its word form.",
                "Many oranges are actually green.",
                "The opposite sides of a die will always add up to seven.",
                "You are 13.8 percent more likely to die on your birthday.",
                "Playing dance music can help ward off mosquitoes.",
                "The King of Hearts is the only king in a deck of cards without a mustache."
                '"Dream" is the only word in the English language that ends with "mt."',
                'A Greek-Canadian man invented the "Hawaiian" pizza (Sam Panopoulos).',
                "If you open your eyes in a pitch-black room, the color you'll see is called 'eigengrau'.",
                "Cats can't taste sweet things because of a genetic defect.",
                "A group of hippos is called a 'bloat.'",
                "Pogonophobia is the fear of beards.",
                "Alaska is the only state whose name is on one row on a keyboard.",
                "The average adult spends more time on the toilet than they do exercising.",
                "Your fingernails grow faster on your dominant hand.",
                "A 'jiffy'' is about one trillionth of a second.",
                "Why were the utensils stuck together?\n**They were spooning.**",
                "Dragonflies have six legs but can't walk.",
                "Golf balls tend to have 336 'dimples.'",
                "Montpelier, Vermont, is the only U.S. capital without a McDonald's.",
                "Apple seeds contain cyanide.",
                "Mulan has the highest kill-count of any Disney character."]
        info_picker = random.choice(info)
        await ctx.send(info_picker)

    @commands.command()
    async def yomama(self, ctx):
        yo_mama = ['Yo momma is so fat when she got on the scale it said, "I need your weight not your phone number."',
                   "Yo momma is so fat, I took a picture of her last Christmas and it's still printing.",
                   'Yo momma is so fat that when she went to the beach a whale swam up and sang, "We are family, even though you are fatter than me."',
                   'Yo mamma is so ugly when she tried to join an ugly contest they said, "Sorry, no professionals."',
                   'Yo momma is so fat her bellybutton gets home 15 minutes before she does.',
                   'Yo momma is so stupid, she put two quarters in her ears and thought she was listening to 50 Cent.',
                   'Yo momma so stupid she stuck a battery up her ass and said, "I GOT THE POWER!"',
                   'Yo momma is so stupid she climbed over a glass wall to see what was on the other side.',
                   'Yo momma is so hairy, when she went to the movie theater to see Star Wars, everybody screamed and said, "IT''S CHEWBACCA!"',
                   'Yo momma iss so dumb, when ya\'ll were driving to Disneyland, she saw a sign that said "Disneyland left," so she went home.',
                   'Yo mama so fat I tried driving around her and I ran out of gas.',
                   'Yo momma is so ugly Fix-It Felix said, "I can\'t fix it."',
                   'Yo momma is so fat she sat on the rainbow and Skittles came out.',
                   'Yo momma is so old, I slapped her in the back and her boobs fell off.',
                   'Yo momma is so ugly she turned Medusa into stone.',
                   'Yo Momma\'s teeth are so yellow, that when she smiles, traffic slows down!',
                   'Yo mama so dark when I clicked on her profile pic, I thought my phone died.',
                   'Yo momma\'s breath smelled so bad when she walked by a clock it said, "Tic Tac?"',
                   'Yo mama so fat, she doesn\'t need internet, she\'s already worldwide.',
                   'Yo momma is so stupid that she sat on the TV to watch the couch.']
        randomMama = random.choice(yo_mama)
        await ctx.send(randomMama)

    @commands.command()
    async def joke(self, ctx):
        await asyncio.sleep(0.5)
        jokes = ["What’s the best thing about Switzerland?\nI don’t know, but the flag is a big plus",
                 "I invented a new word!\n**Plagiarism!**",
                 "Did you hear about the claustrophobic astronaut?\n**He just needed a little space.**",
                 "Why don’t scientists trust atoms?\n**Because they make up everything.**",
                 "Why did the chicken go to the séance?\n**To get to the other side.**",
                 "Have You Heard About the Sick Chemist?\n**If you can't helium, and you can't curium, you'll probably "
                 "have to barium**.",
                 "I'm Reading a Book on Anti-Gravity\n**I can't put it down**.",
                 "Did You Know There's a Band Called 1023MB?\n**They're not bad, but they haven't had any gigs yet**.",
                 "What's Another Name for Santa's Elves?\n**Subordinate Clauses**.",
                 "What kind of noise does a witch’s vehicle make?\n**Brrrroooom, brrroooom**.",
                 "What did one ocean said to the other?\n**Nothing, they just waved**.",
                 "Why do bees have sticky hair?\n**Because they use a honeycomb.**",
                 "I used to hate facial hair, but then it grew on me",
                 "I want to make a brief joke, but it’s a little cheesy.",
                 "5/4 of people admit they’re bad at fractions.",
                 "Why were the utensils stuck together?\n**They were spooning.**",
                 "What kind of shoes does a lazy person wear?\n**Loafers.**",
                 "**Teacher:** Where is the English Channel?\n**Student:** I don't know, my TV doesn't pick it up!",
                 "What do geographers grow in their gardens?\n**Compass roses.**",
                 "What is the fastest country in the world?\n**Russia**",
                 "Why did the football coach went to the bank?\n**To get his quarterback**"]
        jokes_picker = random.choice(jokes)
        await ctx.send(jokes_picker)

def setup(client):
    client.add_cog(meh(client))   #bot.add_cog(mech(bot)) is the name of the cog "mech" must match line 8