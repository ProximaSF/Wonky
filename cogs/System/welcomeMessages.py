import random
import asyncio
import os
import disnake
from disnake.ext import commands
from cogs.System.Webhook import Webhook


class Welcome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        hello_url = ["https://i.gifer.com/M5Kj.gif",
                     "https://media0.giphy.com/media/Rsp9jLIy0VZOKlZziw/giphy.gif?cid=790b7611f4ac2dad9240f4dfc1759846e0d1fd08a9cc3a74&rid=giphy.gif&ct=g",
                     "https://media.tenor.com/pJHrgeFjEF4AAAAM/mecha-smc.gif",
                     "https://media3.giphy.com/media/xUPGGDNsLvqsBOhuU0/giphy.gif?cid=790b7611e5c85b6c5b4af4427645623709abcd7fa5ca4634&rid=giphy.gif&ct=g",
                     "https://i.pinimg.com/originals/75/a9/8b/75a98b0e7f34bb6f69e17e0eee7b2756.gif",
                     "https://media3.giphy.com/media/XD9o33QG9BoMis7iM4/giphy.gif?cid=790b76111f7973c3603c37528bd45bdcae050a9298bbd7f1&rid=giphy.gif&ct=g",
                     "https://media2.giphy.com/media/3orieQHmkjxSiLGC08/giphy.gif?cid=790b7611696efd83235b7de47679a9ec9b9a344432489b48&rid=giphy.gif&ct=g",
                     "https://c.tenor.com/Tad1yOXINzMAAAAC/welcome-party.gif",
                     "https://media.tenor.com/sO7pXz7Bw2MAAAAM/hello-welcome.gif",
                     "https://media.giphy.com/media/xTiIzJSKB4l7xTouE8/giphy.gif"]
        hello_url_picker = random.choice(hello_url)

        guild_id = member.guild.id
        file_path = f"txt/ServerSettings/{guild_id}/welcome_message.txt"

        with open(file_path, 'r+', encoding='utf-8') as f:
            welcome_edit = f.readlines()

        info_line_1 = -1
        for i, line in enumerate(
                welcome_edit):  # Used to detect the keywords so when editing the information, it will be placed
            # at the right location/lines
            if "Info_1:" in line:
                info_line_1 = i
                break

        info_line_2 = -1
        for i, line in enumerate(welcome_edit):
            if "Info_2" in line:
                info_line_2 = i
                break

        welcome_message_line = welcome_edit[2:info_line_1] if info_line_1 > 0 else welcome_edit[2:]
        welcome_message_info = "".join(welcome_message_line).strip()

        info_1_line = welcome_edit[info_line_1 + 1:info_line_2] if info_line_2 > 0 else welcome_edit[info_line_1:]
        info_1_info = "".join(info_1_line).strip()

        info_2_line = welcome_edit[info_line_2 + 1:]
        info_2_info = "".join(info_2_line).strip()

        clientProfilePicture = member.display_avatar.url  # use member.avatar.url for pycharm and member.display_avatar.url for Spark server
        guild = member.guild

        replace = [
            ("[guild.name]", str(guild.name)),
            ("[member.name]", str(member.name))]

        for placeholder, replacement in replace:
            welcome_message_info = welcome_message_info.replace(placeholder, replacement)

        for placeholder, replacement in replace:
            info_1_info = info_1_info.replace(placeholder, replacement)

        for placeholder, replacement in replace:
            info_2_info = info_2_info.replace(placeholder, replacement)

        if member.guild.system_channel is not None:
            def read_welcome_message_status(guild_id):
                file_path = f"txt/ServerSettings/{guild_id}/{guild_id}.txt"
                if os.path.exists(file_path):
                    with open(file_path, "r") as file:
                        for line in file:
                            if "Join Message:" in line:
                                return line.strip().split(":")[1].strip().lower()

            if read_welcome_message_status(member.guild.id) == "true":
                embed = disnake.Embed(title=f"{welcome_message_info}", color=0xffa947)
                embed.set_author(name=f"{member.name}", icon_url=f"{clientProfilePicture}")
                embed.set_image(url=hello_url_picker)
                embed.add_field(name="----------------------------------", value="", inline=True)
                embed.add_field(name="Getting Started:", value=f"{info_1_info}", inline=False)
                embed.add_field(name="----------------------------------", value=f"{info_2_info}", inline=False)
                embed.set_footer(text="Prefix for this bot is `&`")
                await member.guild.system_channel.send(embed=embed)

                title = ''
                message_description = (f"**{member.name}** joined **{guild.name}**\n"
                                       f"**G_ID**: {guild_id}")
                webhook_instance = Webhook()
                webhook_instance.webhook_embed(title, message_description)
                return
            else:
                title = ''
                message_description = (f"**{member.name}** joined **{guild.name}**\n"
                                       f"**G_ID**: {guild_id}")
                webhook_instance = Webhook()
                webhook_instance.webhook_embed(title, message_description)
                return
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild_id = member.guild.id
        guild = member.guild

        def read_welcome_message_status(guild_id):
            file_path = f"txt/ServerSettings/{guild_id}/{guild_id}.txt"
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    for line in file:
                        if "Leave Message:" in line:
                            return line.strip().split(":")[1].strip().lower()

        if read_welcome_message_status(member.guild.id) == "true":
            # Check if the member was banned
            ban_entry = None
            async for entry in member.guild.bans():
                if entry.user == member:
                    ban_entry = entry
                    break

            if ban_entry is not None:
                # Do something when a member is banned from the guild
                banner = None
                for entry in await member.guild.audit_logs(limit=1, action=disnake.AuditLogAction.ban).flatten():
                    if entry.target.id == member.id:
                        banner = entry.user
                        break

                guild = member.guild
                if guild.system_channel is not None:
                    #embed = disnake.Embed(title=f"**{member}** was banned by {banner}", color=0xffa947)
                    #await guild.system_channel.send(embed=embed)
                    title = ''
                    message_description = f"**{member.name}** was banned from **{guild.name}**"
                    webhook_instance = Webhook()
                    webhook_instance.webhook_embed(title, message_description)

            else:
                # Do something when a member leaves the guild voluntarily
                channel = member.guild.system_channel
                if channel is not None:
                    clientProfilePicture = member.display_avatar.url  # use member.avatar.url for pycharm and member.display_avatar.url for Spark server
                    guild = member.guild
                    if guild.system_channel is not None:
                        bye = [f"**{member.name}** found a better place 👋", f"**{member.name}** left us 😢",
                               f"Farewell **{member.name}**", f"{member.name} left the server: It's their loss"]
                        bye_picker = random.choice(bye)

                        embed = disnake.Embed(title=bye_picker, color=0x979c9f)
                        embed.set_author(name=f"{member.name}", icon_url=f"{clientProfilePicture}")
                        bye_url = ["https://media.tenor.com/Arsu0w_nD2EAAAAM/bob-anakshie.gif",
                                   "https://media3.giphy.com/media/8UH02id9Lf78yP9ZmT/giphy.gif?cid=790b7611e7c50531634d6c056817df2559cfbcfdd6cc6ccd&rid=giphy.gif&ct=g",
                                   "https://media.tenor.com/Arsu0w_nD2EAAAAM/bob-anakshie.gif",
                                   "https://media.tenor.com/qYbjnr7Y2S8AAAAM/simpson-bye.gif",
                                   "https://media3.giphy.com/media/OB4Sjggq8aMJnq4sLQ/giphy.gif",
                                   "https://i.kym-cdn.com/photos/images/newsfeed/001/338/313/3cd.gif",
                                   "https://media.tenor.com/i7M6m0lr6bEAAAAM/kitty-kitten.gif",
                                   "https://media.tenor.com/Aoz9_qKxxiIAAAAM/cry-sad.gif",
                                   "https://media1.giphy.com/media/j0gQA2VD38NKc9rc8y/giphy.gif?cid=790b76118fd2a8dce25c0903ed43de771e7ad5ce2de05004&rid=giphy.gif&ct=g",
                                   "https://c.tenor.com/w76k2_LsFyAAAAAC/denzel-curry.gif"]
                        bye_url_picker = random.choice(bye_url)
                        embed.set_image(url=bye_url_picker)

                        await guild.system_channel.send(embed=embed)

                        title = ''
                        message_description = (f"**{member.name}** left **{guild.name}**\n"
                                               f"**G_ID**: {guild_id}")
                        webhook_instance = Webhook()
                        webhook_instance.webhook_embed(title, message_description)
                        return
        else:
            title = ''
            message_description = (f"**{member.name}** left **{guild.name}**\n"
                                   f"**G_ID**: {guild_id}")
            webhook_instance = Webhook()
            webhook_instance.webhook_embed(title, message_description)
            return


    @commands.has_any_role("Admin")
    @commands.command()
    async def EWM(self, ctx):
        try:
            guild_id = ctx.guild.id
            file_path = f"txt/ServerSettings/{guild_id}/welcome_message.txt"

            with open(file_path, 'r+', encoding='utf-8') as f:
                welcome_edit = f.readlines()

            message = await ctx.send(
                f"Before you start editing the welcome embed message, make sure this code is not already running, if it"
                f" is, come back in 1 minute."
                f"\nDo you wish to edit?")

            await message.add_reaction('✔️')
            await message.add_reaction('❌')

            def check(reaction, user):
                return user == ctx.author and reaction.message == message

            reaction = None  # Initialize the 'reaction' variable with None
            try:
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=30.0, check=check)
                await message.clear_reactions()
            except TimeoutError:
                await ctx.send("You took too long to react, command canceled")

            if reaction is not None and str(reaction.emoji) == '✔️':
                await message.delete()

                done_flag = False  # Flag to control the outer loop, if someone want to end the code, done_flag will
                # turn to "True", ending the inner first and than outer loops. You have mutiple layers of loops,
                # it will still end the whole command long as it has done_flag within the loop(s)
                confirm_timer = 60
                editing_timer = 300

                responses_dict = {}

                while not done_flag:
                    message = await ctx.send(
                        f"For your **welcome message**, what do you want it to say when someone join the server?"
                        f"\nIf you want to mention the person who joined, use **[member.name]** as a placeholder"
                        f"\nIf you want to mention the server's name, use **[guild.name]** as a placeholder"
                        f"\nYou may use these placeholder in the next following questions."
                        f"\nType **Skip** to continue to the next input"
                        f"\nType **STOPECODE** to end this command")

                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel

                    welcome_message_msg = None
                    try:
                        welcome_message_msg = await ctx.bot.wait_for('message', check=check, timeout=editing_timer)
                    except asyncio.TimeoutError:
                        await ctx.send("You took too long to respond, command canceled.")
                        done_flag = True  # Set the flag to True to exit the outer loop
                        break

                    if welcome_message_msg.content.lower() == "stopcode":
                        await ctx.send("Command stopped.")
                        is_editing = False
                        done_flag = True  # Set the flag to True to exit the outer loop
                        break

                    elif welcome_message_msg.content.lower() == "skip":
                        for i, line in enumerate(welcome_edit):
                            if "Info_1:" in line:
                                info_1_line_index = i
                                break

                        welcome_message_line = welcome_edit[
                                               2:info_1_line_index] if info_1_line_index > 0 else welcome_edit[2:]
                        welcome_message_info = "".join(welcome_message_line).strip()
                        responses_dict["welcome_message"] = "".join(welcome_message_info)
                        break

                    else:
                        await ctx.send(
                            f"This is the welcome message you added:"
                            f"\nType **yes** to continue"
                            f"\nType **no** to continue editing"
                            f"\nType **stopcode** to end"
                            f"\n---------------------"
                            f"\n{welcome_message_msg.content}"
                            f"\n---------------------")

                        def check_response(m):
                            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in [
                                'yes', 'no', 'stopcode']

                        try:
                            response = await ctx.bot.wait_for('message', check=check_response,
                                                              timeout=confirm_timer)
                        except asyncio.TimeoutError:
                            await ctx.send("You took too long to respond, command canceled.")
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break

                        if response.content.lower() == "yes":
                            responses_dict["welcome_message"] = welcome_message_msg.content
                            break

                        elif response.content.lower() == "stopcode":
                            await ctx.send("Command stopped.")
                            is_editing = False
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break
                        else:
                            await ctx.send("Continuing with the current question.")
                            continue

                # Outer loop continues here for the next question
                if done_flag:
                    return

                while not done_flag:
                    message = await ctx.send(
                        f"For your **welcome message info_1**, what do you want it to be?"
                        f"\nType **Skip** to continue to the next input"
                        f"\nType **STOPECODE** to end this command")

                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel

                    weapon_msg = None
                    try:
                        info_1_msg = await ctx.bot.wait_for('message', check=check, timeout=editing_timer)
                    except asyncio.TimeoutError:
                        await ctx.send("You took too long to respond, command canceled.")
                        done_flag = True  # Set the flag to True to exit the outer loop
                        break

                    if info_1_msg.content.lower() == "stopcode":
                        await ctx.send("Command stopped.")
                        is_editing = False
                        done_flag = True  # Set the flag to True to exit the outer loop
                        break

                    elif info_1_msg.content.lower() == "skip":
                        for i, line in enumerate(welcome_edit):
                            if "Info_1:" in line:
                                info_1_line_index = i
                                break
                        for i, line in enumerate(welcome_edit):
                            if "Info_2:" in line:
                                info_2_line_index = i
                                break

                        info_1_line = welcome_edit[
                                      info_1_line_index + 1:info_2_line_index] if info_2_line_index > 0 else welcome_edit[
                                                                                                             info_1_line_index:]
                        info_1_info = "".join(info_1_line).strip()
                        responses_dict["info_1_message"] = "".join(info_1_info)
                        break

                    else:
                        await ctx.send(
                            f"This is the info_1 message you gave"
                            f"\nType **yes** to submit your responses"
                            f"\nType **no** to continue editing"
                            f"\nType **stopcode** to end code"
                            f"\n---------------------"
                            f"\n{info_1_msg.content}"
                            f"\n---------------------")

                        def check_response(m):
                            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in [
                                'yes', 'no', 'stopcode']

                        try:
                            response = await ctx.bot.wait_for('message', check=check_response,
                                                              timeout=confirm_timer)
                        except asyncio.TimeoutError:
                            await ctx.send("You took too long to respond, command canceled.")
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break

                        if response.content.lower() == "yes":
                            responses_dict["info_1_message"] = info_1_msg.content
                            break

                        elif response.content.lower() == "stopcode":
                            await ctx.send("Command stopped.")
                            is_editing = False
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break

                        else:
                            await ctx.send("Continuing with the current question.")
                            continue
                if done_flag:
                    return

                while not done_flag:
                    message = await ctx.send(
                        f"For your **welcome message info_2**, what do you want it to be?"
                        f"Type **Skip** to skip this option"
                        f"\nType **STOPECODE** to end this command")

                    def check(msg):
                        return msg.author == ctx.author and msg.channel == ctx.channel

                    try:
                        info_2_msg = await ctx.bot.wait_for('message', check=check, timeout=editing_timer)
                    except asyncio.TimeoutError:
                        await ctx.send("You took too long to respond, command canceled.")
                        done_flag = True  # Set the flag to True to exit the outer loop
                        break

                    if info_2_msg.content.lower() == "stopcode":
                        await ctx.send("Command stopped.")
                        is_editing = False
                        done_flag = True  # Set the flag to True to exit the outer loop
                        break

                    elif info_2_msg.content.lower() == "skip":

                        # Find the index where the "welcome_message:" and "info_1:" section starts (if it exists)
                        for i, line in enumerate(welcome_edit):
                            if "Welcome_Message:" in line:
                                welcome_line_index = i
                            elif "Info_1:" in line:
                                info_1_line_index = i
                                break

                        # Remove the lines between "Background:" and "Weapons:"
                        if welcome_line_index != -1 and info_1_line_index != -1: del welcome_edit[
                                                                                     welcome_line_index + 1:info_1_line_index]
                        # Insert the new "Welcome_Message" section
                        welcome_edit.insert(welcome_line_index + 1, f"\n{responses_dict['welcome_message']}\n\n")

                        # Find the index where the "info_1" and "info_2" section starts (if it exists)
                        for i, line in enumerate(welcome_edit):
                            if "Info_1" in line:
                                info_1_line_index = i
                            elif "Info_2" in line:
                                info_2_line_index = i
                                break

                        # Remove the lines between "info_1:" and "info_2:"
                        if info_1_line_index != -1 and info_2_line_index != -1: del welcome_edit[
                                                                                    info_1_line_index + 1:info_2_line_index]
                        # Insert the new "info_1_message" section
                        welcome_edit.insert(info_1_line_index + 1, f"\n{responses_dict['info_1_message']}\n\n")

                        # Write the updated content back to the file
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.writelines(welcome_edit)

                        await ctx.send("Welcome message is now updated, here's what it look like when someone joins:")

                        hello_url = ["https://i.gifer.com/M5Kj.gif"]
                        hello_url_picker = random.choice(hello_url)

                        with open(file_path, 'r', encoding='utf-8') as f:
                            welcome_edit = f.readlines()

                        info_line_1 = -1
                        for i, line in enumerate(welcome_edit):
                            # at the right location/lines
                            if "Info_1:" in line:
                                info_line_1 = i
                                break
                        info_line_2 = -1
                        for i, line in enumerate(welcome_edit):
                            if "Info_2" in line:
                                info_line_2 = i
                                break
                        welcome_message_line = welcome_edit[2:info_line_1] if info_line_1 > 0 else welcome_edit[2:]
                        welcome_message_info = "".join(welcome_message_line).strip()

                        info_1_line = welcome_edit[info_line_1 + 1:info_line_2] if info_line_2 > 0 else welcome_edit[
                                                                                                        info_line_1:]
                        info_1_info = "".join(info_1_line).strip()

                        info_2_line = welcome_edit[info_line_2 + 1:]
                        info_2_info = "".join(info_2_line).strip()

                        clientProfilePicture = ctx.author.display_avatar.url  # use member.avatar.url for pycharm and member.display_avatar.url for Spark server
                        guild = ctx.author.guild

                        embed = disnake.Embed(title=f"{welcome_message_info}", color=0xffa947)
                        embed.set_author(name=f"{ctx.author}", icon_url=f"{clientProfilePicture}")
                        embed.set_image(url=hello_url_picker)

                        embed.add_field(name="----------------------------------",
                                        value="", inline=True)
                        embed.add_field(name="Getting Started:",
                                        value=f"{info_1_info}", inline=False)
                        embed.add_field(name="----------------------------------",
                                        value=f"{info_2_info}", inline=False)
                        embed.set_footer(text="Prefix for this bot is `&`")
                        await ctx.send(embed=embed)

                        is_editing = False
                        done_flag = True  # Set the flag to True to exit the outer loop
                        break

                    else:
                        await ctx.send(
                            f"This is the info_1 message you gave"
                            f"\nType **done** to submit your responses"
                            f"\nType **no** to continue editing"
                            f"\nType **stopcode** to end code"
                            f"\n---------------------"
                            f"\n{info_2_msg.content}"
                            f"\n---------------------")

                        def check_response(m):
                            return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in [
                                'done', 'no', 'stopcode']

                        try:
                            response = await ctx.bot.wait_for('message', check=check_response,
                                                              timeout=confirm_timer)
                        except asyncio.TimeoutError:
                            await ctx.send("You took too long to respond, command canceled.")
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break

                        if response.content.lower() == "done":
                            responses_dict["info_2_message"] = info_2_msg.content

                            # Find the index where the "welcome_message:" and "info_1:" section starts (if it exists)
                            for i, line in enumerate(welcome_edit):
                                if "Welcome_Message:" in line:
                                    welcome_line_index = i
                                elif "Info_1:" in line:
                                    info_1_line_index = i
                                    break

                            # Remove the lines between "Background:" and "Weapons:"
                            if welcome_line_index != -1 and info_1_line_index != -1: del welcome_edit[
                                                                                         welcome_line_index + 1:info_1_line_index]
                            # Insert the new "Welcome_Message" section
                            welcome_edit.insert(welcome_line_index + 1, f"\n{responses_dict['welcome_message']}\n\n")

                            # Find the index where the "info_1" and "info_2" section starts (if it exists)
                            for i, line in enumerate(welcome_edit):
                                if "Info_1" in line:
                                    info_1_line_index = i
                                elif "Info_2" in line:
                                    info_2_line_index = i
                                    break

                            # Remove the lines between "info_1:" and "info_2:"
                            if info_1_line_index != -1 and info_2_line_index != -1: del welcome_edit[
                                                                                        info_1_line_index + 1:info_2_line_index]
                            # Insert the new "info_1_message" section
                            welcome_edit.insert(info_1_line_index + 1, f"\n{responses_dict['info_1_message']}\n\n")

                            for i, line in enumerate(welcome_edit):
                                if "Info_2" in line:
                                    info_2_line_index = i

                            # Remove the lines for "info_2:"
                            del welcome_edit[info_2_line_index + 1:]
                            # Insert the new "info_2_message" section
                            welcome_edit.insert(info_2_line_index + 1, f"\n{responses_dict['info_2_message']}\n\n")

                            # Write the updated content back to the file
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.writelines(welcome_edit)

                            responses_dict["info_2_message"] = info_2_msg.content
                            await ctx.send(
                                "Welcome message is now updated, here's what it look like when someone joins:")

                            hello_url = ["https://i.gifer.com/M5Kj.gif"]
                            hello_url_picker = random.choice(hello_url)

                            with open(file_path, 'r', encoding='utf-8') as f:
                                welcome_edit = f.readlines()

                            info_line_1 = -1
                            for i, line in enumerate(welcome_edit):
                                # at the right location/lines
                                if "Info_1:" in line:
                                    info_line_1 = i
                                    break
                            info_line_2 = -1
                            for i, line in enumerate(welcome_edit):
                                if "Info_2" in line:
                                    info_line_2 = i
                                    break
                            welcome_message_line = welcome_edit[2:info_line_1] if info_line_1 > 0 else welcome_edit[2:]
                            welcome_message_info = "".join(welcome_message_line).strip()

                            info_1_line = welcome_edit[
                                          info_line_1 + 1:info_line_2] if info_line_2 > 0 else welcome_edit[
                                                                                               info_line_1:]
                            info_1_info = "".join(info_1_line).strip()

                            info_2_line = welcome_edit[info_line_2 + 1:]
                            info_2_info = "".join(info_2_line).strip()

                            clientProfilePicture = ctx.author.display_avatar.url  # use member.avatar.url for pycharm and member.display_avatar.url for Spark server
                            guild = ctx.author.guild

                            embed = disnake.Embed(title=f"{welcome_message_info}", color=0xffa947)
                            embed.set_author(name=f"{ctx.author}", icon_url=f"{clientProfilePicture}")
                            embed.set_image(url=hello_url_picker)

                            embed.add_field(name="----------------------------------",
                                            value="", inline=True)
                            embed.add_field(name="Getting Started:",
                                            value=f"{info_1_info}", inline=False)
                            embed.add_field(name="----------------------------------",
                                            value=f"{info_2_info}", inline=False)
                            embed.set_footer(text="Prefix for this bot is `&`")
                            await ctx.send(embed=embed)

                            is_editing = False
                            break
                        elif response.content.lower() == "stopcode":
                            await ctx.send("Command stopped.")
                            is_editing = False
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break
                        else:
                            await ctx.send("Continuing with the current question.")
                            continue
                if done_flag:
                    return
            elif reaction is not None and str(reaction.emoji) == '❌':
                await ctx.send("canceled")

        except Exception as error:
            print(f"{error}")
            await ctx.send(f"Problem: **[{error}]**")
        finally:
            is_editing = False

        print(responses_dict)  # will print all the entries
        print(responses_dict["Welcome_Message"])  # will print entry for weapons
        # print(self.responses_dict[arg]["description"])
        # print(self.responses_dict[arg]["pilot ability"])

    @commands.has_any_role("admin", "Admin")
    @commands.command()
    async def statusWM(self, ctx):
        try:
            await ctx.send("Type **true** to enable welcome message or **false** to disable.")

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            guild_id = ctx.guild.id
            file_path = f"txt/ServerSettings/{guild_id}/{guild_id}.txt"

            msg = await self.client.wait_for('message', check=check)

            if msg.content.casefold() == "true":
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                if os.path.exists(file_path):
                    with open(file_path, "w") as f:
                        for line in lines:
                            if "Join Message:" in line:
                                line = f"Join Message: true\n"
                            f.write(line)

            elif msg.content.casefold() == "false":
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                if os.path.exists(file_path):
                    with open(file_path, "w") as f:
                        for line in lines:
                            if "Join Message:" in line:
                                line = f"Join Message: false\n"
                            f.write(line)
        except Exception as error:
            print(error)

    @commands.has_any_role("admin", "Admin")
    @commands.command()
    async def statusLM(self, ctx):
        try:
            await ctx.send("Type **true** to enable leave message or **false** to disable.")

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel

            guild_id = ctx.guild.id
            file_path = f"txt/ServerSettings/{guild_id}/{guild_id}.txt"

            msg = await self.client.wait_for('message', check=check)

            if msg.content.casefold() == "true":
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                if os.path.exists(file_path):
                    with open(file_path, "w") as f:
                        for line in lines:
                            if "Leave Message:" in line:
                                line = f"Leave Message: true\n"
                            f.write(line)

            elif msg.content.casefold() == "false":
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                if os.path.exists(file_path):
                    with open(file_path, "w") as f:
                        for line in lines:
                            if "Leave Message:" in line:
                                line = f"Leave Message: false\n"
                            f.write(line)
        except Exception as error:
            print(error)

    '''@commands.command()
        async def status(self, ctx):
            guild_id = ctx.guild.id
            file_path = f"txt/ServerSettings/{guild_id}/{guild_id}.txt"
            target_words = ["Join Message", "Leave Message"]

            def find_line_numbers(file_path, target_words):
                line_numbers = {}

                with open(file_path, 'r') as file:
                    for line_number, line in enumerate(file, 1):
                        for target_word in target_words:
                            if target_word in line:
                                line_numbers[target_word] = line_number
                    return line_numbers

            line_numbers = find_line_numbers(file_path, target_words)


            join_message_status_line_number = line_numbers["Join Message"]
            leave_message_status_line_number = line_numbers["Leave Message"]

            with open(file_path, 'r') as f:
                lines = f.readlines()

            join_status = lines[join_message_status_line_number - 1].strip().split(': ')[1].lower()
            leave_status = lines[leave_message_status_line_number - 1].strip().split(': ')[1].lower()

            await ctx.send(f"Welcome message: **{join_status}**\n"
                           f"Leave message: **{leave_status}**")'''
def setup(client):
    client.add_cog(Welcome(client))