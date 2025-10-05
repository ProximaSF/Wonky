import random
import disnake
from disnake.ext import commands
from disnake import Embed, File
from PIL import Image, ImageDraw
from io import BytesIO
import traceback



class interact(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kidnap(self, ctx: commands.Context, member: disnake.Member):
        if member is ctx.author:
            selfkidnap = ["you can't kidnap yourself", f"Someone kidnap {ctx.author.name}",
                          "yeah, it doesn't work like that, find someone to kidnap"]
            random_kidnap = random.choice(selfkidnap)
            await ctx.send(random_kidnap)
        else:
            message = ["Wonder where they went.",
                       f"Hopefully {member.name} is okay 👀",
                       f"What did {member.name} do this time?",
                       f"Will, it was nice knowing you {member.name} 👋",
                       f'"My precious!"',
                       f"Perhaps it was a friendly kidnap?",
                       "There they go.",
                       f"Maybe {ctx.author.name} is taking {member.name} to a better place.",
                       "At least we know who kidnapped who"]
            message_random = random.choice(message)
            embed = disnake.Embed(title=f"{ctx.author.name} just kidnapped {member.name}: {message_random}",
                                   color=disnake.Color.orange())
            kidnap_url = [
                "https://c.tenor.com/Cw35mhUJCu4AAAAM/dap2.gif",
                "http://i0.kym-cdn.com/photos/images/original/000/979/391/bd5.gif",
                "https://pa1.narvii.com/6487/8fd37c497bf80f02c5e5675823ddbf46e09dfa2d_hq.gif",
                "https://pa1.narvii.com/5779/1cf73775ed0d97fb718e776efdf24f40e99b841a_hq.gif",
                "https://media.tenor.com/aLviAF7W5lUAAAAi/catnap-kidnap.gif",
                "https://64.media.tumblr.com/20005d8464c481a10e2b2afc47a58fe2/6cf83635b93cee52-f2/s540x810/16d64bb9f4f0443472b182b6c63aa53eff804378.gif"]
            kidnap_random = random.choice(kidnap_url)
            embed.set_image(url=kidnap_random)
            await ctx.send(embed=embed)

    @commands.command()
    async def tackle(self, ctx: commands.Context, member: disnake.Member):
        if member is ctx.author:
            selftackle = ["You tackled yourself... how does that work?", f"Someone tackle {ctx.author.name}", "TF 😕"]
            random_tackle = random.choice(selftackle)
            await ctx.send(random_tackle)
        else:
            randomMember = random.choice(ctx.guild.members)
            message = ["That look hurt!.",
                       f"Hopefully {member.name} is okay 👀",
                       f"What did {member.name} do this time?",
                       f"Maybe they were playing football?",
                       f'"DAMN!"',
                       f"Perhaps it was a friendly tackle?",
                       "Oof!",
                       f"But why?",
                       f"YIKES! Glad {randomMember.name} wasn't it."]
            message_random = random.choice(message)
            embed = disnake.Embed(title=f"{ctx.author.name} just tackled {member.name}! {message_random}",
                                   color=disnake.Color.orange())
            tackle_url = [
                "https://media.tenor.com/7CeI4Tsmz7QAAAAC/anime-tackle.gif",
                "https://c.tenor.com/bCgwHwoF1kEAAAAC/old-man-anime.gif",
                "https://thumbs.gfycat.com/ImpracticalBothLeonberger-max-1mb.gif",
                "https://gifimage.net/wp-content/uploads/2017/09/anime-tackle-gif-2.gif",
                "https://media.tenor.com/4XVx7XQSboMAAAAM/kitsune-upload-tackle.gif",
                "https://pa1.narvii.com/5700/dbe48bdcf2a71cfde4c296063f4f9a1cfcb4d1c5_hq.gif"]
            tackle_random = random.choice(tackle_url)
            embed.set_image(url=tackle_random)
            await ctx.send(embed=embed)

    @commands.command()
    async def bash(self, ctx: commands.Context, member: disnake.Member):
        if member is ctx.author:
            message = ["Don't bash yourself again if you don't want me to bash you!",
                       f"Hopefully {member.name} is okay 👀",
                       f'"Oof"',
                       "There you go",
                       f"{member.name} is done for.",
                       "RIP."]
            message_random = random.choice(message)
            embed = disnake.Embed(title=f"Wonky bashed {ctx.author.name}: {message_random}",
                                   color=disnake.Color.orange())
            bash_url = [
                "https://i.pinimg.com/originals/99/7a/80/997a804ba20b96a9dc0af3543de4b3ca.gif",
                "https://i.gifer.com/7zBH.gif",
                "https://64.media.tumblr.com/a7cc25e4e84bd6b8b66df34c41928ec7/b0973cc81a6dce27-3a/s540x810/4b258dc35248cfdc11d7055c99f9fc7712a40275.gif",
                "https://i.pinimg.com/originals/71/f2/28/71f2287429a4fc3cef551dfb7d3d33a8.gif",
                "https://media.tenor.com/FJsjk_9b_XgAAAAC/anime-hit.gif"]
            bash_random = random.choice(bash_url)
            embed.set_image(url=bash_random)
            selfbash = ["You bashed yourself... okay...?", f"You must be sad, let me bash for you", "TF 😕",
                        f"someone please bash {ctx.author.name}", "you need attention?"]
            random_bash = random.choice(selfbash)
            if random.choice(selfbash) == "You must be sad, let me bash for you":
                await ctx.send("You must be sad, let me bash for you")
                await ctx.send(embed=embed)
            else:
                await ctx.send(random_bash)
        else:
            message = ["That look hurt.",
                       f"Hopefully {member.name} is okay 👀",
                       f"What did {member.name} do this time?",
                       f"What's their beef?",
                       f'"Oof"',
                       f"Perhaps it was out of love...",
                       "There they go.",
                       f"{member.name} is done for.",
                       "RIP.",
                       f"Poor {member.name}"]
            message_random = random.choice(message)
            embed = disnake.Embed(title=f"{ctx.author.name} bashed {member.name}: {message_random}",
                                   color=disnake.Color.orange())
            bash_url = [
                "https://i.pinimg.com/originals/99/7a/80/997a804ba20b96a9dc0af3543de4b3ca.gif",
                "https://i.gifer.com/7zBH.gif",
                "https://64.media.tumblr.com/a7cc25e4e84bd6b8b66df34c41928ec7/b0973cc81a6dce27-3a/s540x810/4b258dc35248cfdc11d7055c99f9fc7712a40275.gif",
                "https://i.pinimg.com/originals/71/f2/28/71f2287429a4fc3cef551dfb7d3d33a8.gif",
                "https://media.tenor.com/FJsjk_9b_XgAAAAC/anime-hit.gif"]
            bash_random = random.choice(bash_url)
            embed.set_image(url=bash_random)
            await ctx.send(embed=embed)

    @commands.command()
    async def lick(self, ctx: commands.Context, member: disnake.Member):
        if member is ctx.author:
            selflick = [f"You just licked, yourself... gay..?", "ayo, trying to get horny?",
                        f"Someone pleas lick {ctx.author.name}, it might taste good",
                        f"I would lick you but the programmer is too lazy to add a message and a gif of me (Wonky) licking you"]
            randomselflick = random.choice(selflick)
            await ctx.send(randomselflick)
        else:
            message = ["Oh my...",
                       f"Hopefully {ctx.author.name} isn't sick👀",
                       f"What did {member.name} do this time?",
                       f"I know you want some of that",
                       f'"Noice!"',
                       f"Perhaps it was out of love... 🤷",
                       "What's next?",
                       f"Who will {ctx.author.name} lick next or was {member.name} the only person he/she was after?",
                       "Why?",
                       f"Luck bastard"]
            message_random = random.choice(message)
            embed = disnake.Embed(title=f"{ctx.author.name} licked {member.name}: {message_random}",
                                   color=disnake.Color.orange())
            lick_url = [
                "https://media.tenor.com/S5I9g4dPRn4AAAAM/omamori-himari-manga.gif",
                "https://media.tenor.com/S5I9g4dPRn4AAAAM/omamori-himari-manga.gif",
                "https://i.gifer.com/8Zwm.gif",
                "https://media.giphy.com/media/UhSNkDdbsXzlm/giphy.gif",
                "https://media.tenor.com/Go7wnhOWjSkAAAAC/anime-lick-face.gif"]
            bash_random = random.choice(lick_url)
            embed.set_image(url=bash_random)
            await ctx.send(embed=embed)

    @commands.command()
    async def dance(self, ctx: commands.Context, member: disnake.Member = None):
        if not member or member is ctx.author:
            message = ["That look fun",
                       f"🎵Cha Cha Real Smooth🎵",
                       f"You got some moves {ctx.author.name}",
                       f"Owo",
                       f'I see you',
                       f"Cringe",
                       "Wish I can move like that 👀"]
            message_random = random.choice(message)
            embed = disnake.Embed(title=f"{ctx.author.name} is dancing: {message_random}",
                                   color=disnake.Color.orange())
            selfdance_url = [
                "https://media.tenor.com/LP6rGpITvlsAAAAM/chill.gif",
                "https://i.pinimg.com/originals/11/e9/03/11e9038965932e27306b6c8ef16bd574.gif",
                "https://media.tenor.com/UcB2uIbChAsAAAAC/anime-boy.gif",
                "https://media.tenor.com/xHdQRsnCSVYAAAAM/kakashi-dancing.gif",
                "https://media.tenor.com/jWRFHjiNdkgAAAAd/anime-dance.gif",
                "https://media.tenor.com/2vRn7mgoMRMAAAAC/cute-anime-dance.gif",
                "https://c.tenor.com/0VqODsv_QqIAAAAC/dance-dance-revolution-levi.gif"]
            bash_random = random.choice(selfdance_url)
            embed.set_image(url=bash_random)
            await ctx.send(embed=embed)
        else:
            message = ["That look fun",
                       f"🎵Cha Cha Real Smooth🎵",
                       f"They got some moves - DAMN!",
                       f"Owo",
                       f'Who\'s next?',
                       f"Cringe",
                       "Wish I can move like that 👀"]
            message_random = random.choice(message)
            embed = disnake.Embed(title=f"{ctx.author.name} is dancing with {member.name}: {message_random}",
                                   color=disnake.Color.orange())
            dance_url = [
                "https://media1.giphy.com/media/euMGM3uD3NHva/giphy.gif?cid=790b7611c3ec446564845fc53091fd11916b4c21c220d399&rid=giphy.gif&ct=g",
                "https://media1.giphy.com/media/y5efFpqW5knlu/giphy.gif?cid=790b76118f2a64fde04eb98a937896edeaf1333f2f6b01c7&rid=giphy.gif&ct=g",
                "https://media3.giphy.com/media/mJIa7rg9VPEhzU1dyQ/giphy.gif?cid=790b7611415c00b3e806b0c9d0e11c17f38837ff196334d0&rid=giphy.gif&ct=g",
                "https://wallpapercave.com/uwp/uwp608254.gif",
                "https://i.pinimg.com/originals/03/6d/d2/036dd2045bd45d4866ddb4dcb516a76f.gif"]
            bash_random = random.choice(dance_url)
            embed.set_image(url=bash_random)
            await ctx.send(embed=embed)

    @commands.command()
    async def gift(self, ctx: commands.Context, member: disnake.Member):
        if member is ctx.author:
            message = ["There you go 😊", "This is all I have", "You poor thing", "It not money but it will do"]
            message_random = random.choice(message)
            embed = disnake.Embed(title=f"Wonky gave {member.name} a gift: {message_random}",
                                   color=disnake.Color.orange())
            gift_url = [
                "https://c.tenor.com/DfxFTn5tcwIAAAAd/orange-anime-kakeru-naruse.gif",
                "https://giffiles.alphacoders.com/198/198766.gif",
                "https://image.myanimelist.net/ui/5pjpFizOF0WqHWXSGonzMRiNJD0LnM9ffyHAtIEkVxqTkpiTH5viVRnMvNaCsf8VKuLvX-7EV9P_Gx1kB7vDbZ3uA-pa5hkrbKkktiuhZQk",
                "https://i.pinimg.com/originals/cc/a8/43/cca843053f03f657543ea56643975f70.gif",
                "https://68.media.tumblr.com/0dd8516bc850158a6bf24d158e552c14/tumblr_o8owayVK2o1vwyx4qo1_540.gif",
                "https://pa1.narvii.com/5791/bd42f498e76f2805348fc44f9e8ead74d16ea6ad_hq.gif",
                "https://thumbs.gfycat.com/BronzePeacefulHogget-max-1mb.gif",
                "https://i.imgur.com/Mr6zdgJ.gif"]
            gift_random = random.choice(gift_url)
            embed.set_image(url=gift_random)

            selfgift = ["You gave yourself a gift, did you use shadow clone jutsu?",
                        "I can't watch this - I'll give you a gift",
                        "Wow, you must be lonely", f"Someone give this person a gift - smhs, or something",
                        "you poor thing"]
            random_selfgift = random.choice(selfgift)
            if random.choice(selfgift) == "I can't watch this - I'll give you a gift":
                await ctx.send(embed=embed)
                await ctx.send("I can't watch this - I'll give you a gift")
            else:
                await ctx.send(random_selfgift)
        else:
            message = ["aw 😊",
                       f"Wonder what it was... 🤔",
                       f"{member.name} must be really special!",
                       f"Are you a sugar daddy/queen {ctx.author.name}?",
                       f'"Noice!"',
                       f"What's next?",
                       f"OwO",
                       f"Gimme!!",
                       f"Luck bastard"]
            message_random = random.choice(message)
            embed = disnake.Embed(title=f"{ctx.author.name} gave {member.name} a gift: {message_random}",
                                   color=disnake.Color.orange())
            gift_url = [
                "https://c.tenor.com/DfxFTn5tcwIAAAAd/orange-anime-kakeru-naruse.gif",
                "https://giffiles.alphacoders.com/198/198766.gif",
                "https://image.myanimelist.net/ui/5pjpFizOF0WqHWXSGonzMRiNJD0LnM9ffyHAtIEkVxqTkpiTH5viVRnMvNaCsf8VKuLvX-7EV9P_Gx1kB7vDbZ3uA-pa5hkrbKkktiuhZQk",
                "https://i.pinimg.com/originals/cc/a8/43/cca843053f03f657543ea56643975f70.gif",
                "https://68.media.tumblr.com/0dd8516bc850158a6bf24d158e552c14/tumblr_o8owayVK2o1vwyx4qo1_540.gif",
                "https://pa1.narvii.com/5791/bd42f498e76f2805348fc44f9e8ead74d16ea6ad_hq.gif",
                "https://thumbs.gfycat.com/BronzePeacefulHogget-max-1mb.gif",
                "https://i.imgur.com/Mr6zdgJ.gif"]
            gift_random = random.choice(gift_url)
            embed.set_image(url=gift_random)
            await ctx.send(embed=embed)

    @commands.command()
    async def pmessage(self, ctx: commands.Context, *, arg):  # use * to combine combine words into one arg
        everyone = "@everyone"
        if everyone in arg:
            await ctx.send("You're not allowed to ping everyone using this command!", delete_after=3)
        else:
            message = ctx.message
            await message.delete()
            embed = disnake.Embed(title=f'Anonymous: "{arg}"', color=disnake.Color.orange())
            await ctx.send(embed=embed)
            print(f'{ctx.author.display_name} sent "{arg}"')

    @commands.command()
    async def avatar(self, ctx: commands.Context, member: disnake.Member = None):
        """TOP: member is just a name, can be anything. Without 'None', it will not show the arthur's avatar if he/she do not input a username"""
        author = ctx.author

        if not member:
            member = author  # Get your avatar if you do not mention someone

            Avatarurl = member.display_avatar.url  # <--- Use member.avatar_url for pycharm and member.display_avatar.url for Spark server

            embed = disnake.Embed(title=f"Your avatar:", color=disnake.Color.orange())
            embed.set_image(url=Avatarurl)
            await ctx.send(embed=embed)
            # await ctx.send("{}'s avatar: {}".format(member.name, Avatarurl))
        else:
            Avatarurl = member.display_avatar.url  # <--- Use member.avatar_url for pycharm and member.display_avatar.url for Spark server
            embed = disnake.Embed(title=f"{ctx.author.name} want to see {member.name}'s avatar:",
                                   color=disnake.Color.orange())
            embed.set_image(url=Avatarurl)
            await ctx.send(embed=embed)

    @commands.command()
    async def wanted(self, ctx, user: disnake.Member = None):
        if user == None:
            user = ctx.author

        wanted = Image.open("images/wanted.png")

        # file = disnake.File("images/coin_head.png")

        data = BytesIO(await user.display_avatar.read())
        pfp = Image.open(data)

        pfp = pfp.resize((741, 945))

        wanted.paste(pfp, (629, 853))
        wanted.save("images/profile.png")

        await ctx.send(file=disnake.File("images/profile.png"))

    @commands.command()
    async def head(self, ctx, user: disnake.Member = None):
        user = random.choice(ctx.guild.members)

        wanted = Image.open("images/hangman/hangman_empty.png")

        # file = disnake.File("images/coin_head.png")

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
        wanted.paste(result, (430, 290), result)
        wanted.save("images/hangman/changes/hangman_head.png")

        await ctx.send(file=disnake.File("images/hangman/changes/hangman_head.png"))

        try:
            f = disnake.File("images/hangman/changes/hangman_head.png", filename="hangman_head.png")
            embed = disnake.Embed(title='HANGMAN')
            embed.set_image(url="attachment://hangman_head.png")

            await ctx.send(file=f, embed=embed)


        except Exception as error:
            error_info = traceback.format_exc()
            await ctx.send(f"Error: {error}")
            print(f"Error: {error}\n{error_info}")

            return


def setup(client):
    client.add_cog(interact(client))  # bot.add_cog(mech(bot)) is the name of the cog "mech" must match line 8
