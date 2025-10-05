import asyncio
import shutil
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
import tracemalloc
import os
import re

# Import other cogs
from cogs.System.Webhook import Webhook

tracemalloc.start()  # Get error message
load_dotenv()
intents = disnake.Intents.all()
intents.members = True  # Welcome/leave message
intents.bans = True

prefix = "&"
client = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)
client.remove_command('help')


def send_webhook_message(title, message_description):
    webhook_instance = Webhook()
    webhook_instance.webhook_embed(title, message_description)
    return


# Load cog files
def load_cogs(command_type: str) -> None:
    title = ''
    message_description = ''
    for filename in os.listdir(f"./cogs/{command_type}"):
        if filename.endswith(".py"):
            extension = filename[:-3]
            try:
                client.load_extension(f"cogs.{command_type}.{extension}")
                message_description += f"Loaded extension '{extension}'\n"
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                message_description += f'Failed to load extension {extension}\n{exception}'

    send_webhook_message(title, message_description)


# This will automatically load slash commands and normal commands located in their respective folder.
if __name__ == "__main__":
    load_cogs("Slash")
    load_cogs("Normal")
    load_cogs("System")


def create_guild_folder_and_content(guild_id, guild_name):
    # create a new folder named after the guild id
    guild_directory = f'txt/ServerSettings/{guild_id}'

    os.mkdir(guild_directory)

    # create a new txt file in the folder just created based on the guild id
    guild_settings = f'txt/ServerSettings/{guild_id}'
    file_name = os.path.join(guild_settings, f"{guild_id}.txt")

    # Add content inside the new guild_id txt file for settings based on the server_settings_template.txt
    with open("txt/server_setting_template.txt", "r") as file:
        server_settings_template = file.read().strip()
        server_settings_template = server_settings_template.replace("Server_ID", str(guild_id))
        server_settings_template = server_settings_template.replace("Server_Name", guild_name)
    with open(file_name, 'w') as file:
        file.writelines(server_settings_template)

    # Copy the content of welcome_message_template.txt to welcome_message.txt
    source_file = "txt/welcome_message_template.txt"
    destination_file = os.path.join(guild_settings, "welcome_message.txt")
    shutil.copyfile(source_file, destination_file)

    # Create im_joke.txt
    im_joke_path = f'txt/ServerSettings/{guild_id}/im_joke.txt'
    open(im_joke_path, 'w')


@client.event
async def on_ready():
    print(f"I am ready to go - {client.user.name} 👍")
    await client.change_presence(
        activity=disnake.Activity(type=disnake.ActivityType.watching,
                                  name=f"water get wet | {prefix}help"))

    title = f'{client.user.name} is now 🟢'
    message_description = ''
    send_webhook_message(title, message_description)

    def update_wordle_game_status_to_false():
        for guild in client.guilds:
            guild_id = guild.id
            file_path = f"txt/ServerSettings/{guild_id}/{guild_id}.txt"
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                with open(file_path, "w") as f:
                    for line in lines:
                        if "Word Games:" in line:
                            line = "Word Games: false\n"
                        f.write(line)
            else:
                pass
        return

    def add_user_info_to_playerpoints():
        # Add new user info to playerpoints if it doesn't exist
        for guild in client.guilds:
            members = guild.members

            with open("txt/playerpoints.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()

            for member in members:
                if member.bot:
                    continue  # If user is a bot, skip to the next member
                user_found = any(f"[{member.id}]" in line for line in lines)
                if not user_found:  # If user not found
                    # Add the user to the playerpoints.txt file
                    with open("txt/user_template.txt", "r") as t:
                        user_template = t.read().strip()
                        user_template = user_template.replace("user_id",
                                                              str(member.id))  # Replace user_id with the member's ID
                        user_template = user_template.replace("user_name",
                                                              member.name)  # Replace user_name with the member's name
                        lines.append(user_template + "\n\n")

            # Write the new user info to the playerpoints.txt file
            with open("txt/playerpoints.txt", "w", encoding="utf-8") as f:
                f.writelines(lines)

    def create_guild_folder():
        for guild in client.guilds:
            guild_directory = f'txt/ServerSettings/{guild.id}'
            if os.path.exists(guild_directory):
                im_joke_path = f'txt/ServerSettings/{guild.id}/im_joke.txt'
                if os.path.exists(im_joke_path):
                    pass
                else:
                    # create a im_joke.txt file in guild directory if does not exist
                    im_joke_file_name = os.path.join(im_joke_path)
                    open(im_joke_file_name, 'w+')
            else:
                guild_id = guild.id
                guild_name = guild.name
                create_guild_folder_and_content(guild_id, guild_name)

    def add_latest_item_to_guild_settings():
        # Add the last item from server_settings_template.txt to all the guild settings
        for guild in client.guilds:
            template_path = f"txt/server_setting_template.txt"
            guild_setting_txt = f"txt/ServerSettings/{guild.id}/{guild.id}.txt"
            items = []

            if os.path.exists(guild_setting_txt):  # if guild folder exist, return and do nothing

                with open(template_path, "r") as file:
                    lines = file.readlines()
                last_item = lines[-1]
                last_item_split = last_item.strip().split(':')[0].strip()
                # print(last_item_split)

                with open(guild_setting_txt, 'r') as file:
                    lines = file.readlines()
                    for i in lines:
                        items.append(i.strip().split(':')[0].strip())
                    # print(items)
                    if last_item_split in items:
                        # print("Already up to date")
                        pass
                    else:
                        with open(guild_setting_txt, 'a') as f:
                            f.write(f'{last_item}')
            else:
                guild_id = guild.id
                guild_name = guild.name
                create_guild_folder_and_content(guild_id, guild_name)
                print(f"{guild.id} folder was missing")
                pass

    update_wordle_game_status_to_false()
    add_latest_item_to_guild_settings()
    add_user_info_to_playerpoints()
    create_guild_folder()


@client.event
async def on_guild_join(guild):
    guild_directory = f'txt/ServerSettings/{guild.id}'
    if os.path.exists(guild_directory):  # if guild folder exist, return and do nothing
        return
    else:
        guild_id = guild.id
        guild_name = guild.name
        create_guild_folder_and_content(guild_id, guild_name)


@commands.has_any_role("admin", "Admin")
@client.command()
async def sinfo(ctx):
    guild_id = ctx.guild.id
    msg = ''
    file_path = f'txt/ServerSettings/{guild_id}/{guild_id}.txt'
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for items in lines:
        if items.startswith("Server ID"):
            msg += f"Server: {ctx.guild}\n"
            pass
        else:
            msg += items

    embed = disnake.Embed(title=f"Server Settings Info", color=disnake.Color.orange())
    embed.add_field(name='', value=msg)
    await ctx.send(embed=embed)



@client.command()
async def help(ctx):
    total_pages = "5"

    page1 = embed = disnake.Embed(title=f'Wonky\'s Command Menu', color=disnake.Color.orange())
    embed.add_field(name="Prefix for this bot is &", value="------------------------------------", inline=True)
    embed.add_field(name='😐 Meh Commands',
                    value='`flip "h" or "t"`\n`joke`\n`guess`\n`useless_info`\n`yomama`\n'
                          '`ttt`\n`ngg`\n`trivia`\n`immsg`\n`wuwa_gacha`\n`gacha_sim`', inline=False)
    embed.set_footer(text=f"Made by: ProximaSF. Wonky is in ♾ servers. 'Page 1/{total_pages}'")

    page2 = embed = disnake.Embed(title=f'Wonky\'s Command Menu', color=disnake.Color.orange())
    embed.add_field(name="Prefix for this bot is &", value="------------------------------------", inline=True)
    embed.add_field(name="😏 Actions",
                    value='`kidnap`\n`tackle`\n`bash`\n`lick`\n`gift`\n`dance`\n`pmessage "your message"`\n'
                          '`avatar`\n`steal @user {amount} 50 max`\n`steal {amount} 50 max`\n`steal @user {amount}`', inline=False)
    embed.set_footer(text=f"Made by: ProximaSF. Wonky is in ♾ servers. 'Page 2/{total_pages}'")

    page3 = embed = disnake.Embed(title=f'Wonky\'s Command Menu', color=disnake.Color.orange())
    embed.add_field(name="Prefix for this bot is &", value="------------------------------------", inline=True)
    embed.add_field(name="🤖 Super Mecha Champions",
                    value='`challenge`\n`v4vxv`\n`mech "name"`\n`edit "name"`', inline=False)
    embed.set_footer(text=f"Made by: ProximaSF. Wonky is in ♾ servers. 'Page 3/{total_pages}'")

    page4 = embed = disnake.Embed(title=f'Wonky\'s Command Menu', color=disnake.Color.orange())
    embed.add_field(name="Prefix for this bot is &", value="------------------------------------", inline=True)
    embed.add_field(name="⚙ System Commands",
                    value='`help`\n`reminder`\n`clear`\n`invite`\n`playground_help`\n`start_playground`\n'
                          '`stop_playground`\n`leader`\n`info @user`\n`EWM`\n`statusWM`\n`statusLM`\n`wordc "word"`\n'
                          '`getLword`\n`addword "a word"`\n`sinfo`\n`EstatusIM`',
                    inline=False)
    embed.set_footer(text=f"Made by: ProximaSF. Wonky is in ♾ servers. 'Page 4/{total_pages}'")

    page5 = embed = disnake.Embed(title=f'Wonky\'s Command Menu', color=disnake.Color.orange())
    embed.add_field(name="Prefix for this bot is &", value="------------------------------------", inline=True)
    embed.add_field(name="📔 Future Commands",
                    value='`Poll`\n`Dice`\n`Music`\n`kick/ban`\n`IDK`', inline=False)
    embed.set_footer(text=f"Made by: ProximaSF. [Page 5/{total_pages}]")
    # embed.set_footer(text=f"Made by: ProximaSF. Wonky is in {len(client.guilds)} servers. 'Page 5/{total_pages}'")

    pages = [page1, page2, page3, page4, page5]

    message = await ctx.send(embed=page1)
    await message.add_reaction('⏮')
    await message.add_reaction('◀')
    await message.add_reaction('▶')
    await message.add_reaction('⏭')

    def check(reaction, user):
        return user == ctx.author and reaction.message == message

    i = 0
    reaction = None

    while True:
        if str(reaction) == '⏮':
            i = 0
            await message.edit(embed=pages[i])
        elif str(reaction) == '◀':
            if i > 0:
                i -= 1
                await message.edit(embed=pages[i])
        elif str(reaction) == '▶':
            if i < 4:
                i += 1
                await message.edit(embed=pages[i])
        elif str(reaction) == '⏭':
            i = 4
            await message.edit(embed=pages[i])

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=120.0, check=check)
            await message.remove_reaction(reaction, user)
        except:
            break
    #await message.edit(embed=page1)    Change page after timer ends
    await message.clear_reactions()


@client.command()
async def immsg(ctx):
    guild_id = ctx.guild.id
    file_path = f"txt/ServerSettings/{guild_id}/im_joke.txt"

    im_msg_dict = {}
    im_msg = ''
    num = 0
    immsg_nums = 0
    dict_num = 1
    line_num = 0

    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Store all the im messages into a dictionary, divided by 5 messages per key
    while line_num < len(lines):
        line = lines[line_num]
        if line.startswith('**['):
            num += 1
            immsg_nums += 1
            im_msg += f"{immsg_nums}: {line} {lines[line_num + 1]}\n"
            line_num += 2
        else:
            line_num += 1

        # Add 5 msg to dictionary and check if there's any remaining message that wasn't added
        if num == 5 or line_num >= len(lines):
            im_msg_dict[dict_num] = im_msg
            num = 0
            im_msg = ''
            dict_num += 1

    # Grab messages based on key(page_value) asked
    def embed_page_msg(page_value):
        embed = disnake.Embed(title="I'm Messages", color=disnake.Color.green())
        embed.add_field(name='', value=im_msg_dict[page_value], inline=False)
        return embed

    page1 = embed = disnake.Embed(title="I'm Messages", color=disnake.Color.green())
    embed.add_field(name='', value=im_msg_dict[1], inline=False)
    message = await ctx.send(embed=page1)

    await message.add_reaction('⏮')
    await message.add_reaction('◀')
    await message.add_reaction('▶')
    await message.add_reaction('⏭')

    def check(reaction, user):
        return user == ctx.author and reaction.message == message

    i = 0 + 1
    reaction = None

    while True:
        if str(reaction) == '⏮':
            i = 0 + 1
            await message.edit(embed=embed_page_msg(i))
        elif str(reaction) == '◀':
            if i > 0 + 1:
                i -= 1
                await message.edit(embed=embed_page_msg(i))
        elif str(reaction) == '▶':
            if i < len(im_msg_dict):
                i += 1
                await message.edit(embed=embed_page_msg(i))
        elif str(reaction) == '⏭':
            i = len(im_msg_dict)
            await message.edit(embed=embed_page_msg(i))

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=120.0, check=check)
            await message.remove_reaction(reaction, user)
        except:
            break
    # await message.edit(embed=page1)
    await message.clear_reactions()


@client.command()
async def info(ctx, user: disnake.Member):
    if user is None:
        user = ctx.author
    with open("txt/playerpoints.txt", "r") as f:
        lines = f.readlines()
        f.seek(0)
        for i, line in enumerate(lines):
            if str(user.id) in line:
                WobbleBit_line = lines[i + 1]
                current_WobbleBits = int(WobbleBit_line.strip().split(': ')[1])

                health_line = lines[i + 2]
                current_health = int(health_line.strip().split(': ')[1])

                attempts_line = lines[i + 3]
                current_steal_attempts = int(attempts_line.strip().split(': ')[1])

                clientProfilePicture = user.display_avatar.url
                embed = disnake.Embed(title=f"{user.name}'s Info", color=disnake.Color.orange())
                embed.set_author(name=f"{user.name}", icon_url=f"{clientProfilePicture}")

                embed.add_field(name='', value=
                f"\n➡ Wobble Bit(s): {current_WobbleBits}\n"
                f"\n➡ Health Attempts: {current_health}\n"
                f"\n➡ Steal Attempts: {current_steal_attempts}\n"
                f"\n➡ Bio: ...", inline=False)
                await ctx.send(embed=embed)
                return
        await ctx.send(f"{user.mention} doesn't have any Wobble Bit.")


@client.command()
async def leader(ctx):
    # Open the text file and read its contents
    with open('txt/playerpoints.txt', 'r') as file:
        file_content = file.read()

    # Use a regular expression to find all user IDs and points in the file
    user_WobbleBits = re.findall(r'\[(\d+)\]: (.+?)\n\s+Current WobbleBits: (\d+)', file_content)

    # Create a dictionary to store the points for each user ID
    WobbleBits_dict = {}
    for user_id, username, WobbleBits in user_WobbleBits:
        WobbleBits_dict[user_id] = int(WobbleBits)

    # Sort the dictionary by the points in descending order
    sorted_dict = dict(sorted(WobbleBits_dict.items(), key=lambda x: x[1], reverse=True))

    # Create the leaderboard message
    leaderboard_message = "\n"
    rank = 1
    for user_id, WobbleBits in list(sorted_dict.items())[:10]:
        user = await client.fetch_user(int(user_id))
        leaderboard_message += f"{rank}. {user.name} - {WobbleBits} WobbleBits\n\n"
        rank += 1

    # Send the leaderboard message to the Discord channel
    embed = disnake.Embed(title="Leaderboard", description=leaderboard_message, color=disnake.Color.orange())
    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    try:
        value_delete = 10
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Must have the role titled `Admin` to use this command", delete_after=value_delete)
            await asyncio.sleep(value_delete)
            await ctx.message.delete()
        if isinstance(error, commands.MissingAnyRole):
            await ctx.send("Must have the role titled `Admin` to use this command", delete_after=value_delete)
            await asyncio.sleep(value_delete)
            await ctx.message.delete()
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("That was not a command, type `&help` for a list of commands", delete_after=value_delete)
            await asyncio.sleep(value_delete)
            await ctx.message.delete()
    except Exception as error:
        print(f"{error}")
        await ctx.send(f"Problem: **[{error}]**", delete_after=value_delete)

client.run("")    # Wonky



