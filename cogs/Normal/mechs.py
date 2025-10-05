import asyncio
import ntpath
import random
import time
import datetime
from datetime import datetime
import disnake
from disnake.ext import commands
from disnake.ext.commands import check

from dotenv import load_dotenv
import os
from os import getenv
import re
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint

from PIL import Image
from io import BytesIO


class mech(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.responses_dict = {}
        self.is_editing = False

    @commands.command()
    async def mech(self, ctx, *, arg):
        if self.is_editing:
            await ctx.send(f"Embed for {arg} is offline because of editing")
            return

        mech_list = ["Arthur", "Snow", "Hotsteel", "Raven", "Gabriel", "Pulsar", "Michael", "Hurricane", "Boltus",
                     "Ranger", "Trio", "Firefox", "Fire Star", "Aurora", "Caramel", "Trio", "Skylark", "Andromeda",
                     "Doomlight", "Ventorus", "Northern Knight", "Flamenco", "Neutron", "Alborada", "Jojo", "Skyfall",
                     "Akashic", "Dreadwolf", "Death Knell", "Moon Rabbit", "Pulsar", "Raven"]

        total_pages = "7"

        mech_colors = [("firefox", (251, 48, 58)), ("arthur", (255, 255, 255)), ("caramel", (245, 177, 95)),
                       ("skylark", (158, 252, 251)), ("hotsteel", (248, 79, 36)), ("andromeda", (245, 138, 168)),
                       ("gabriel", (134, 124, 193)), ("doomlight", (121, 158, 107)), ("hurricane", (9, 49, 140)),
                       ("raven", (100, 100, 140)), ("ventorus", (144, 51, 53)), ("boltus", (232, 200, 112)),
                       ("aurora", (90, 71, 104)), ("snow", (255, 255, 255)), ("pulsar", (255, 255, 255)),
                       ("dreadwolf", (255, 255, 255)), ("ranger", (255, 255, 255)), ("jojo", (255, 255, 255)),
                       ("skyfall", (255, 255, 255)), ("michael", (255, 255, 255)), ("flamenco", (255, 255, 255)),
                       ("akashic", (255, 255, 255)), ]

        try:
            if self.is_editing:
                await ctx.send(f"Embed for {arg} is offline because of editing")
                return
            if arg.casefold() == "trio of enders" or arg.casefold() == "trio of ender" or arg.casefold() == "trio":
                mech = "Trio of Enders"
                r = int(161)
                b = int(138)
                g = int(84)

                page1 = embed = disnake.Embed(title=f'{mech}: Discription',
                                               color=disnake.Color.from_rgb(r, b, g))
                embed.add_field(name="Background:",
                                value='"Trio of Ender, it\'s the most intoxicating symphony of distruction ever played in the SMC area!" '
                                      'The ability to switch between three primary weapons; assault rifle, shotgun and rocket launcher gives Trio the ability to to bully any mech at any given place: '
                                      'long, medium or short range. Activating its tactical ability, '
                                      'Trio enters assault mode, giving the ability to automatically fire all primary weapons at the same time, while boosting jump height and significantly '
                                      'increasse movement speed!', inline=False)
                embed.set_image(
                    url="https://cdn.discordapp.com/attachments/892316788468101200/1061837417830678618/TrioOfEnder.jpeg")
                embed.set_footer(text=f'Page 1/{total_pages}')

                page2 = embed = disnake.Embed(title=f'{mech}: Weapons',
                                               color=disnake.Color.from_rgb(r, b, g))
                embed.add_field(name="Shotgun",
                                value='- Mainly used for close-range combat.'
                                      '\n\n'
                                      '- With default settings, it fires 1.7 shots/second or 16 bullets per shot.'
                                      '\n\n'
                                      '- Slowest fire rate and highest bullet spread.'
                                      '\n\n'
                                      '- Due to this, using this in close combat is crucial to deal the most damage.'
                                      '\n\n'
                                      '- Recommend not using shotgun against a full opponent. Rather, use to finish off an opponent (bellow 50% DUR).'
                                      '\n\n'
                                      '- The slower and bigger the target, the easier for you to hit your opponent; mech like firefox.txt, '
                                      'Hotsteel, Kuma or Fire Star are great targets for Trio'
                                , inline=False)
                embed.add_field(name="Assault Rifle",
                                value='- Good for mid-range and occasionally short-range.'
                                      '\n\n'
                                      '- With default settings, it fires 10 shots/second.'
                                      '\n\n'
                                      '- This weapons is good all around except for long-range; use rocket launcher.'
                                      '\n\n'
                                      '- Before closing in on your enemy, try to bring down their health with assault rifle or rocket launcher.'
                                      '\n\n'
                                      '- Out of all the three weapons, I highly recommend use this weapon against fast moving targets like Michael, Skylark, Neutron, Ranger and etc.'
                                      '\n\n'
                                      '- Not recommend using against pilots.'
                                , inline=False)
                embed.add_field(name="Rocket Launcher",
                                value='- Mostly used for long-range combat but also useful in mid and close-range.'
                                      '\n\n'
                                      '- With default, it fires 2 shots/second. Despite this, it have a fast travel speed and fires straight, great for hitting far targets.'
                                      '\n\n'
                                      '- Only weapon that can do area of effect (AOE). Due do this, it is highly recommend used against pilots '
                                      'and mech/pilots that like to hide and poke.'
                                      '\n\n'
                                      '- Similarly to the shotgun\'s fire rate, it is less but still recommend against slow and large opponents.'
                                      '\n\n'
                                      '- Mentioned already, recommend using against mech that like to stay afar or just far away in general like Gabriel, Raven, Snow and Gaesar.'
                                , inline=False)
                embed.add_field(name="Reference",
                                value='Bellow is a chart showing how long it takes to demech Hotsteel without tech, mods or any damage buffs (reloading is included).'
                                , inline=False)

                embed.set_image(
                    url="https://cdn.discordapp.com/attachments/892316788468101200/1061910623283326986/TrioDemech.jpg")
                embed.set_footer(text=f'Page 2/{total_pages}')

                page3 = embed = disnake.Embed(title=f'{mech}: Tactical Ability',
                                               color=disnake.Color.from_rgb(r, b, g))
                embed.add_field(name="Assault Mode:",
                                value='- Trio\'s tactical/combat ability, not secondary (which is switching between weapons).'
                                      '\n\n'
                                      '- Activating Assault mode, Trio moves 32.5%-33.5% faster for 6.5s!'
                                      '\n\n'
                                      '- Great for getting across a TDM map at the very beginning of a match. Also great for getting around'
                                      'in BR maps, running away, closing in on target or dodging (adding jumps too).'
                                      '\n\n'
                                      '- It can finish off any mech in one charge.Recommend having shotgun ready to finish your opponent off quickly in close range'
                                      'if you weren\'t able to.'
                                      '\n\n'
                                      '- Reference: It can kill a Hotsteel in 6.8 seconds.'
                                , inline=False)
                embed.set_footer(text=f'Page 3/{total_pages}')

                page4 = embed = disnake.Embed(title=f'**Trio of Enders**: Builds',
                                               color=disnake.Color.from_rgb(r, b, g))
                embed.add_field(name="Tech & Core Modules:",
                                value='- Recommend using __Transformation Offense__, __Flawless Defence__,  __High Speed Transformation__ as tech modules and __Enhancement Trio__ for core module. '
                                      'This module build is mainly for those who like to switch weapons, gaining the benefits of switch like increase damage, shield gain, faster switching and '
                                      'other buffs from __Enhancement Trio__.'
                                      '\n\n'
                                      '- If you like to use a specifics weapon most of the time or like to reload, a reload module build would be a good choice; using __enhanced Reload__ (faster reload), '
                                      '__Tactical Adjustment__ (restore shield after reloading), __High Speed__ (faster weapon switch) as tech and __Doomsday Symphony__ '
                                      '(Shoot missiles after reload) as core module.'
                                      '\n\n'
                                      '- You may want to use __Enhanced Thread__ if you want better mobility and longer usage time in assault mode. But due to Trio\'s uniqueness, I suggest stick with '
                                      '__High Speed__ for faster switching.'
                                      '\n\n'
                                      '- Regardless of your play style, find what works for you. If you can\' decide, try and balance it out.'
                                , inline=False)
                embed.add_field(name="Techs:",
                                value='- Like modules, build something that you like and works for you. '
                                      '\n\n'
                                      '- I suggest balance it out, but try to avoid tech that include damage boost based on your distance and durability, __Area of Explosion__, __Shot Velocity__ and damage reductions since trio is more of a burst mech.'
                                      '\n\n'
                                      '- If you\'re using the weapon switch module build, use techs that have __Combat/Tactical Skill Recovery__, __Rate of Fire__, __Life Drain__ or __Max Fuel__ or __Fuel Recovery__.'
                                      '\n\n'
                                      '- If you like mobility, go for movement speed, fuel and __Combat Skill Recovery__."'
                                      '\n\n'
                                      '- If you have good aim and like to deal more damage or using a reload module build, go for __Rate of Fire__, __Reload Rate__ techs and something to help you survive longer or increase fuel.',
                                inline=False)
                embed.set_footer(text=f'Page 4/{total_pages}')

                page5 = embed = disnake.Embed(title=f'{mech}: Mech Pilots Abilities',
                                               color=disnake.Color.from_rgb(r, b, g))
                embed.add_field(name="Expeditious Charge and Hovering Attack",
                                value='- If you can shoot while jumping at the same time, these two pilot ability is great, as it provide'
                                      'additional fuel or damage when jumping.', inline=False)
                embed.add_field(name="Damage:",
                                value='- With __Extreme Firepower__, you\'ll able to deal more damage the lower your health is. '
                                      'This ability is mostly useful in TDM.'
                                      '\n\n'
                                      '- __Lightning Mantra__ attack any mech/pilot after activating assault mode/tactical ability. Especially useful against pilots in both BR and TDM; '
                                      'allowing you to accidentally killing a pilot or locating a pilot that is hiding near you.',
                                inline=False)
                embed.add_field(name="Mobility::",
                                value='- __Combat Control__ and __Pursuit Program__ are great abilities that provide better mode mobilities.'
                                      '\n\n'
                                      '- __Wing of Swiftness__ and __Instant Flash__ can provide passive speed boost if you take damage (once every 6s) or switching your weapons (once every 9.5s-7s). ',
                                inline=False)
                embed.add_field(name="Avoid These Abilities:",
                                value='- Any reload abilities. You can use it and it might be useful but the likelihood of using the same weapon for more than 10s is unpractical, unless you\'re not moving or '
                                      'you\'re fighting the same opponent at the same distance.'
                                      '\n\n'
                                      '- Any damage abilities with cooldown or range based like __Shadow Hunter__, __Chain Electroshock__ and __Fatal Verdict__. Since you\'ll be moving '
                                      'most of the time and all of Trio\'s attacks have fairly fast fire rate.',
                                inline=False)
                embed.set_footer(text=f'Page 5/{total_pages}')

                page6 = embed = disnake.Embed(title=f'{mech}: Basic Approach',
                                               color=disnake.Color.from_rgb(r, b, g))
                embed.add_field(name="Basic Approach",
                                value='- When fighting opponent afar, use Rocket Launcher to effectively poke them with high velocity rockets. '
                                      'Also switch to easily deal with pilots.'
                                      '\n\n'
                                      '- Use Assault Rifle to precisely hit your target as you or your opponent moves towards each other. Also against more smaller and maneuverable targets.'
                                      '\n\n'
                                      '- Use shotgun when you\'re close to your enemy or quickly switch to finish off your enemy if they\'re low'
                                      '\n\n'
                                      '- Use Trio\'s tactical/combat ability to deal more burst and move faster.'
                                      'Try to jump while shooting (especially with Shotgun and Assault Rifle) to dodge incoming attacks since'
                                      '\n\n'
                                      'Trio is a large target and moves fairly slow without its tactical ability.'
                                      '\n\n'
                                      '- If you have to reload but your opponent is fairly low and close to you and you\'re using __High Speed__, don\'t reload, instead '
                                      'quickly switch to the next weapon (will be pre-loaded and take only less than 1 second)!'
                                      '\n\n'
                                      '- But if you don\'t or have reload abilities from modules or pilots, reload if you have the appropriate weapon.'
                                , inline=False)
                embed.set_footer(text=f'Page 6/{total_pages}')

                page7 = embed = disnake.Embed(title=f'{mech} Editor(s):',
                                               color=disnake.Color.from_rgb(r, b, g))
                embed.add_field(name=f"",
                                value=f'proximasf#0'
                                , inline=False)
                embed.set_footer(text=f'Page 7/{total_pages}')

                pages = [page1, page2, page3, page4, page5, page6, page7]

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
                        if i < 6:
                            i += 1
                            await message.edit(embed=pages[i])
                    elif str(reaction) == '⏭':
                        i = 6
                        await message.edit(embed=pages[i])

                    try:
                        reaction, user = await self.client.wait_for('reaction_add', timeout=120.0, check=check)
                        await message.remove_reaction(reaction, user)
                    except:
                        break
                await message.edit(embed=page1)
                await message.clear_reactions()

            elif arg is not None and arg.lower() in [mech.lower() for mech in mech_list]:
                self.responses_dict[arg] = {}  # Initialize an empty dictionary for this mech
                # Rest of your code remains the same, starting from mech_name_all_lower = arg.casefold()
                found_mech_color = None
                for mech, colors in mech_colors:
                    if mech == arg.casefold():
                        found_mech_color = colors
                        break

                r = found_mech_color[0]
                b = found_mech_color[1]
                g = found_mech_color[2]

                mech_name_all_lower = arg.casefold()
                # Capitalize the first letter
                mech_name = mech_name_all_lower.capitalize()
                with open(f"cogs/MechInfo/{mech_name_all_lower}.txt", "r") as f:
                    mech_edit = f.readlines()

                # ------------------------------------------------------------------------ #will send out the information for the mech
                weapons_line_index = -1
                for i, line in enumerate(
                        mech_edit):  # Used to detect the keywords so when editing the information, it will be placed
                    # at the right location/lines
                    if "Weapons:" in line:
                        weapons_line_index = i
                        break

                tactical_ability_line_index = -1
                for i, line in enumerate(mech_edit):
                    if "Tactical Ability:" in line:
                        tactical_ability_line_index = i
                        break

                builds_line_index = -1
                for i, line in enumerate(mech_edit):
                    if "Builds:" in line:
                        builds_line_index = i
                        break

                mech_pilot_ability_line_index = -1
                for i, line in enumerate(mech_edit):
                    if "Best Pilot Ability:" in line:
                        mech_pilot_ability_line_index = i
                        break

                overall_approach_line_index = -1
                for i, line in enumerate(mech_edit):
                    if "Overall Approach:" in line:
                        overall_approach_line_index = i
                        break

                edit_arthurs_line_index = -1
                for i, line in enumerate(mech_edit):
                    if "Edited By:" in line:
                        edit_arthurs_line_index = i
                        break

                background_line = mech_edit[2:weapons_line_index] if weapons_line_index > 0 else mech_edit[2:]
                background_info = "".join(background_line).strip()

                weapons_line = mech_edit[
                               weapons_line_index + 1:tactical_ability_line_index] if tactical_ability_line_index > 0 else mech_edit[
                                                                                                                           weapons_line_index:]
                weapons_info = "".join(weapons_line).strip()

                tactical_ability_line = mech_edit[
                                        tactical_ability_line_index + 1:builds_line_index] if builds_line_index > 0 else mech_edit[
                                                                                                                         tactical_ability_line_index:]
                tactical_ability_info = "".join(tactical_ability_line).strip()

                build_line = mech_edit[
                             builds_line_index + 1:mech_pilot_ability_line_index] if mech_pilot_ability_line_index > 0 else mech_edit[
                                                                                                                            builds_line_index:]
                build_info = "".join(build_line).strip()

                best_pilot_line = mech_edit[
                                  mech_pilot_ability_line_index + 1:overall_approach_line_index] if overall_approach_line_index > 0 else mech_edit[
                                                                                                                                         mech_pilot_ability_line_index:]
                best_pilot_info = "".join(best_pilot_line).strip()

                overall_approach_line = mech_edit[
                                        overall_approach_line_index + 1:edit_arthurs_line_index] if edit_arthurs_line_index > 0 else mech_edit[
                                                                                                                                     overall_approach_line_index:]
                overall_approach_info = "".join(overall_approach_line).strip()

                edit_author_line = mech_edit[edit_arthurs_line_index + 1:]
                edit_author_info = "".join(edit_author_line).strip()

                # ------------------------------------------------------------------------

                page1 = embed = disnake.Embed(title=f'{mech_name}: Background',
                                               color=disnake.Color.from_rgb(r, b, g))
                embed.add_field(name="",
                                value=f'{background_info}', inline=False)

                page2 = embed = disnake.Embed(title=f'{mech_name}: Weapons',
                                               color=disnake.Color.from_rgb(r, b, g))
                embed.add_field(name="",
                                value=f'{weapons_info}', inline=False)
                embed.set_footer(text=f'Page 2/{total_pages}')

                page3 = embed = disnake.Embed(title=f'{mech_name}: Tactical Ability',
                                               color=disnake.Color.from_rgb(r, b, g))
                embed.add_field(name="",
                                value=f'{tactical_ability_info}'
                                , inline=False)

                embed.set_footer(text=f'Page 3/{total_pages}')

                page4 = embed = disnake.Embed(title=f'{mech_name}: Builds',
                                               color=disnake.Color.from_rgb(r, b, g))
                embed.add_field(name="",
                                value=f'{build_info}'
                                , inline=False)
                embed.set_footer(text=f'Page 4/{total_pages}')

                page5 = embed = disnake.Embed(title=f'{mech_name}: Pilot Abilities',
                                               color=disnake.Color.from_rgb(r, b, g))
                embed.add_field(name="",
                                value=f'{best_pilot_info}'
                                , inline=False)
                embed.set_footer(text=f'Page 5/{total_pages}')

                page6 = embed = disnake.Embed(title=f'{mech_name}: Overall Approach',
                                               color=disnake.Color.from_rgb(r, b, g))
                embed.add_field(name="",
                                value=f'{overall_approach_info}'
                                , inline=False)
                embed.set_footer(text=f'Page 6/{total_pages}')

                page7 = embed = disnake.Embed(title=f'{mech_name} Editors:',
                                               color=disnake.Color.from_rgb(r, b, g))
                embed.add_field(name=f"",
                                value=f'{edit_author_info}'
                                , inline=False)
                embed.set_footer(text=f'Page 7/{total_pages}')

                pages = [page1, page2, page3, page4, page5, page6, page7]

                message = await ctx.send(embed=page1)
                await message.add_reaction('⏮')
                await message.add_reaction('◀')
                await message.add_reaction('▶')
                await message.add_reaction('⏭')
                await message.add_reaction('❌')

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
                        if i < 6:
                            i += 1
                            await message.edit(embed=pages[i])
                    elif str(reaction) == '⏭':
                        i = 6
                        await message.edit(embed=pages[i])
                    elif str(reaction) == '❌':
                        await message.remove_reaction(reaction, user)
                        break
                    try:
                        reaction, user = await self.client.wait_for('reaction_add', timeout=40.0, check=check)
                        await message.remove_reaction(reaction, user)
                    except:
                        break
                await message.edit(embed=page1)
                await message.clear_reactions()
            else:
                await ctx.send(f"{arg} is not a mech.")

        except Exception as error:
            print(f"{error}")
            await ctx.send(f"Problem: **[{error}]**")

        # Start the background task
        asyncio.ensure_future(self.check_is_editing(ctx))

    @commands.command()
    async def edit(self, ctx, *, arg):
        mech_list = ["Arthur", "Snow", "Hotsteel", "Raven", "Gabriel", "Pulsar", "Michael", "Hurricane", "Boltus",
                     "Ranger", "Trio", "Firefox", "Fire Star", "Aurora", "Caramel", "Trio", "Skylark", "Andromeda",
                     "Doomlight", "Ventorus", "Northern Knight", "Flamenco", "Neutron", "Alborada", "Jojo", "Skyfall",
                     "Akashic", "Dreadwolf", "Death Knell", "Moon Rabbit", "Pulsar", "Raven"]

        try:
            if arg is not None and arg.lower() in [mech.lower() for mech in mech_list]:
                self.is_editing = True  # Set the flag to True to indicate editing process started

                mech_name_all_lower = arg.casefold()
                # Capitalize the first letter
                mech_name = mech_name_all_lower.capitalize()

                with open(f"cogs/MechInfo/{mech_name_all_lower}.txt", 'r') as f:
                    mech_edit = f.readlines()

                background_line_index = -1
                weapons_line_index = -1
                tactical_ability_line_index = -1
                builds_line_index = -1
                mech_pilot_ability_line_index = -1
                overall_approach_line_index = -1
                edit_arthurs = -1

                message = await ctx.send(
                    f"Before you start editing, look at the informations already provided (if any) for the "
                    f"mech you're about to edit by typing **&edit {mech_name}** so you know what to "
                    f"__add__ or __improve__ so players will know how to use the mech properly."
                    f"\nYou will be asked to fill **6** information for {mech_name}. Please use "
                    f"**&mech trio** to see an example of information you will need to provide."
                    f"\n\n***MAKE SURE THE MECH YOU'RE TRYING TO EDIT IS NOT RUNNING, MEANING "
                    f"THERE IS NO REACTION ARROWS UNDERNEATH THE __{mech_name}__ EMBED WHEN SOMEONE USED __&mech {mech_name}__ OR ELSE"
                    f"THIS CODE WILL NOT FUNCTION PROPERLY. COME BACK LATER OR WAIT FOR IT TO END (ABOUT 2 MINUTES).**"
                    f"\nDo you wish to edit the information for **{mech_name}**?")

                await message.add_reaction('✔️')
                await message.add_reaction('❌')

                def check(reaction, user):
                    return user == ctx.author and reaction.message == message

                reaction = None  # Initialize the 'reaction' variable with None
                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=60.0, check=check)
                    await message.clear_reactions()
                except TimeoutError:
                    await ctx.send("You took too long to react, command canceled")

                if reaction is not None and str(reaction.emoji) == '✔️':

                    done_flag = False  # Flag to control the outer loop, if someone want to end the code, done_flag will
                    # turn to "True", ending the inner first and than outer loops. You have mutiple layers of loops,
                    # it will still end the whole command long as it has done_flag within the loop(s)
                    confirm_timer = 300
                    editing_timer = 600
                    if arg not in self.responses_dict:
                        self.responses_dict[arg] = {}

                    while not done_flag:
                        message = await ctx.send(
                            f"Type in the **description** for the mecha **{mech_name}**. Type **STOPCODE** to end the command or **SKIP** to skip this option.")

                        def check(msg):
                            return msg.author == ctx.author and msg.channel == ctx.channel

                        description_msg = None
                        try:
                            description_msg = await self.client.wait_for('message', check=check, timeout=editing_timer)
                        except asyncio.TimeoutError:
                            await ctx.send("You took too long to respond, command canceled.")
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break

                        if description_msg.content.lower() == "stopcode":
                            await ctx.send("Command stopped.")
                            self.is_editing = False
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break
                        elif description_msg.content.lower() == "skip":

                            for i, line in enumerate(
                                    mech_edit):  # Used to detect the keywords so when editing the information, it will be placed
                                # at the right location/lines
                                if "Weapons:" in line:
                                    weapons_line_index = i
                                    break
                            background_line = mech_edit[2:weapons_line_index] if weapons_line_index > 0 else mech_edit[
                                                                                                             2:]
                            background_info = "".join(background_line).strip()
                            self.responses_dict[arg]["description"] = "".join(background_info)
                            break

                        else:
                            await ctx.send(
                                f"This is the description you added for **{mech_name}**."
                                f"\nType **yes** to continue"
                                f"\nType **no** to continue editing"
                                f"\nType **stopcode** to end")

                            embed1 = disnake.Embed(title=f'{mech_name}: Background',
                                                    color=disnake.Color.from_rgb(100, 100, 100))
                            embed1.add_field(name="",
                                             value=f'{description_msg.content}', inline=False)
                            embed1.set_footer(text=f'Page 1/7')
                            await ctx.send(embed=embed1)

                            def check_response(m):
                                return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in [
                                    'yes', 'no', 'stopcode']

                            try:
                                response = await self.client.wait_for('message', check=check_response,
                                                                      timeout=confirm_timer)
                            except asyncio.TimeoutError:
                                await ctx.send("You took too long to respond, command canceled.")
                                done_flag = True  # Set the flag to True to exit the outer loop
                                break

                            if response.content.lower() == "yes":
                                self.responses_dict[arg]["description"] = description_msg.content

                                '''for i, line in enumerate(mech_edit):
                                    if "Background:" in line:
                                        background_line_index = i
                                    elif "Weapons:" in line:
                                        weapons_line_index = i
                                        break

                                # Remove the lines between "Background:" and "Weapons:"
                                if background_line_index != -1 and weapons_line_index != -1:
                                    del mech_edit[background_line_index + 1:weapons_line_index]

                                # Insert the new "Background" section
                                mech_edit.insert(background_line_index + 1,f"\n{self.responses_dict[arg]['description']}\n\n")

                                # Write the updated content back to the file
                                with open(f"cogs/MechInfo/{mech_name}.txt", 'w') as f:
                                    f.writelines(mech_edit)'''

                                break

                            elif response.content.lower() == "stopcode":
                                await ctx.send("Command stopped.")
                                self.is_editing = False
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
                            f"Type in the **weapon** descriptions for **{mech_name}**. Type **STOPCODE** to end the command or **SKIP** to skip this option.")

                        def check(msg):
                            return msg.author == ctx.author and msg.channel == ctx.channel

                        weapon_msg = None
                        try:
                            weapon_msg = await self.client.wait_for('message', check=check, timeout=editing_timer)
                        except asyncio.TimeoutError:
                            await ctx.send("You took too long to respond, command canceled.")
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break

                        if weapon_msg.content.lower() == "stopcode":
                            await ctx.send("Command stopped.")
                            self.is_editing = False
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break
                        elif weapon_msg.content.lower() == "skip":

                            for i, line in enumerate(
                                    mech_edit):  # Used to detect the keywords so when editing the information, it will be placed
                                # at the right location/lines
                                if "Weapons:" in line:
                                    weapons_line_index = i
                                    break
                            for i, line in enumerate(mech_edit):
                                if "Tactical Ability:" in line:
                                    tactical_ability_line_index = i
                                    break

                            weapons_line = mech_edit[
                                           weapons_line_index + 1:tactical_ability_line_index] if tactical_ability_line_index > 0 else mech_edit[
                                                                                                                                       weapons_line_index:]
                            weapons_info = "".join(weapons_line).strip()
                            self.responses_dict[arg]["weapons"] = "".join(weapons_info)
                            break

                        else:
                            await ctx.send(
                                f"This is the weapon(s) description you added for **{mech_name}**."
                                f"\nType **yes** to continue"
                                f"\nType **no** to continue editing"
                                f"\nType **stopcode** to end")

                            embed2 = disnake.Embed(title=f'{mech_name}: Weapons',
                                                    color=disnake.Color.from_rgb(100, 100, 100))
                            embed2.add_field(name="",
                                             value=f'{weapon_msg.content}', inline=False)
                            embed2.set_footer(text=f'Page 2/7')
                            await ctx.send(embed=embed2)

                            def check_response(m):
                                return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in [
                                    'yes', 'no', 'stopcode']

                            try:
                                response = await self.client.wait_for('message', check=check_response,
                                                                      timeout=confirm_timer)
                            except asyncio.TimeoutError:
                                await ctx.send("You took too long to respond, command canceled.")
                                done_flag = True  # Set the flag to True to exit the outer loop
                                break

                            if response.content.lower() == "yes":
                                self.responses_dict[arg]["weapons"] = weapon_msg.content

                                # Find the index where the "Background:" and "Weapons:" section starts (if it exists)
                                '''weapons_line_index = -1
                                tactical_ability_line_index = -1
                                for i, line in enumerate(mech_edit):
                                    if "Weapons:" in line:
                                        weapons_line_index = i
                                    elif "Tactical Ability:" in line:
                                        tactical_ability_line_index = i
                                        break

                                # Remove the lines between "Background:" and "Weapons:"
                                if weapons_line_index != -1 and tactical_ability_line_index != -1:
                                    del mech_edit[weapons_line_index + 1:tactical_ability_line_index]

                                # Insert the new "Background" section
                                mech_edit.insert(weapons_line_index + 1,f"\n{self.responses_dict[arg]['weapons']}\n\n")

                                # Write the updated content back to the file
                                with open(f"cogs/MechInfo/{mech_name}.txt", 'w') as f:
                                    f.writelines(mech_edit)'''

                                break
                            elif response.content.lower() == "stopcode":
                                await ctx.send("Command stopped.")
                                self.is_editing = False
                                done_flag = True  # Set the flag to True to exit the outer loop
                                break
                            else:
                                await ctx.send("Continuing with the current question.")
                                continue
                    if done_flag:
                        return

                    while not done_flag:
                        message = await ctx.send(
                            f"Type in the **tactical ability(s)** descriptions for **{mech_name}**. Type **STOPCODE** to end the command or **SKIP** to skip this option.")

                        def check(msg):
                            return msg.author == ctx.author and msg.channel == ctx.channel

                        tactical_ability_msg = None
                        try:
                            tactical_ability_msg = await self.client.wait_for('message', check=check,
                                                                              timeout=editing_timer)
                        except asyncio.TimeoutError:
                            await ctx.send("You took too long to respond, command canceled.")
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break

                        if tactical_ability_msg.content.lower() == "stopcode":
                            await ctx.send("Command stopped.")
                            self.is_editing = False
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break
                        elif tactical_ability_msg.content.lower() == "skip":
                            for i, line in enumerate(mech_edit):
                                if "Tactical Ability:" in line:
                                    tactical_ability_line_index = i
                                    break
                            for i, line in enumerate(mech_edit):
                                if "Builds:" in line:
                                    builds_line_index = i
                                    break

                            tactical_ability_line = mech_edit[
                                                    tactical_ability_line_index + 1:builds_line_index] if builds_line_index > 0 else mech_edit[
                                                                                                                                     tactical_ability_line_index:]
                            tactical_ability_info = "".join(tactical_ability_line).strip()
                            self.responses_dict[arg]["tactical ability"] = "".join(tactical_ability_info)
                            break
                        else:
                            await ctx.send(
                                f"This is the description you gave for **{mech_name}'s tactical ability(s)**."
                                f"\nType **yes** to continue"
                                f"\nType **no** to continue editing"
                                f"\nType **stopcode** to end")

                            embed3 = disnake.Embed(title=f'{mech_name}: Tactical Ability',
                                                    color=disnake.Color.from_rgb(100, 100, 100))
                            embed3.add_field(name="",
                                             value=f'{tactical_ability_msg.content}', inline=False)
                            embed3.set_footer(text=f'Page 3/7')
                            await ctx.send(embed=embed3)

                            def check_response(m):
                                return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in [
                                    'yes', 'no', 'stopcode']

                            try:
                                response = await self.client.wait_for('message', check=check_response,
                                                                      timeout=confirm_timer)
                            except asyncio.TimeoutError:
                                await ctx.send("You took too long to respond, command canceled.")
                                done_flag = True  # Set the flag to True to exit the outer loop
                                break

                            if response.content.lower() == "yes":
                                self.responses_dict[arg]["tactical ability"] = tactical_ability_msg.content

                                '''# Find the index where the "Tactical Ability:" and "Builds:" section starts (if it exists)
                                for i, line in enumerate(mech_edit):
                                    if "Tactical Ability:" in line:
                                        tactical_ability_line_index = i
                                    elif "Builds:" in line:
                                        builds_line_index = i
                                        break
                                # Remove the lines between "Tactical Ability:" and "Builds:"
                                if tactical_ability_line_index != -1 and builds_line_index != -1:
                                    del mech_edit[tactical_ability_line_index + 1:builds_line_index]
                                # Insert the new "Tactical Ability" section
                                mech_edit.insert(tactical_ability_line_index + 1,f"\n{self.responses_dict[arg]['tactical ability']}\n\n")

                                # Write the updated content back to the file
                                with open(f"cogs/MechInfo/{mech_name}.txt", 'w') as f:
                                    f.writelines(mech_edit)'''

                                break
                            elif response.content.lower() == "stopcode":
                                await ctx.send("Command stopped.")
                                self.is_editing = False
                                done_flag = True  # Set the flag to True to exit the outer loop
                                break
                            else:
                                await ctx.send("Continuing with the current question.")
                                continue

                    if done_flag:
                        return

                    while not done_flag:
                        message = await ctx.send(
                            f"Type in some good **build(s) (techs, modules and cores)** for **{mech_name}**. Type **STOPCODE** to end the command or **SKIP** to skip this option.")

                        def check(msg):
                            return msg.author == ctx.author and msg.channel == ctx.channel

                        build_msg = None
                        try:
                            build_msg = await self.client.wait_for('message', check=check, timeout=editing_timer)
                        except asyncio.TimeoutError:
                            await ctx.send("You took too long to respond, command canceled.")
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break

                        if build_msg.content.lower() == "stopcode":
                            await ctx.send("Command stopped.")
                            self.is_editing = False
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break
                        elif build_msg.content.lower() == "skip":

                            for i, line in enumerate(mech_edit):
                                if "Builds:" in line:
                                    builds_line_index = i
                                    break
                            for i, line in enumerate(mech_edit):
                                if "Best Pilot Ability:" in line:
                                    mech_pilot_ability_line_index = i
                                    break

                            build_line = mech_edit[
                                         builds_line_index + 1:mech_pilot_ability_line_index] if mech_pilot_ability_line_index > 0 else mech_edit[
                                                                                                                                        builds_line_index:]
                            build_info = "".join(build_line).strip()
                            tactical_ability_info = "".join(tactical_ability_line).strip()
                            self.responses_dict[arg]["build"] = "".join(build_info)
                            break
                        else:
                            await ctx.send(
                                f"This is the description you gave for **{mech_name}'s tactical ability(s)**"
                                f"\nType **yes** to continue"
                                f"\nType **no** to continue editing"
                                f"\nType **stopcode** to end")

                            embed4 = disnake.Embed(title=f'{mech_name}: Builds',
                                                    color=disnake.Color.from_rgb(100, 100, 100))
                            embed4.add_field(name="",
                                             value=f'{build_msg.content}', inline=False)
                            embed4.set_footer(text=f'Page 4/7')
                            await ctx.send(embed=embed4)

                            def check_response(m):
                                return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in [
                                    'yes', 'no', 'stopcode']

                            try:
                                response = await self.client.wait_for('message', check=check_response,
                                                                      timeout=confirm_timer)
                            except asyncio.TimeoutError:
                                await ctx.send("You took too long to respond, command canceled.")
                                done_flag = True  # Set the flag to True to exit the outer loop
                                break

                            if response.content.lower() == "yes":
                                self.responses_dict[arg]["build"] = build_msg.content

                                '''# Find the index where  "Builds:" and "Mech Pilot Ability:" section starts (if it exists)
                                for i, line in enumerate(mech_edit):
                                    if "Builds:" in line:
                                        builds_line_index = i
                                    elif "Best Pilot Ability:" in line:
                                        mech_pilot_ability_line_index = i
                                        break

                                # Remove the lines between "Builds:" and "Mech Pilot Ability:"
                                if builds_line_index != -1 and mech_pilot_ability_line_index != -1:
                                    del mech_edit[builds_line_index + 1:mech_pilot_ability_line_index]

                                # Insert the new "Builds" section
                                mech_edit.insert(builds_line_index + 1,f"\n{self.responses_dict[arg]['build']}\n\n")

                                # Write the updated content back to the file
                                with open(f"cogs/MechInfo/{mech_name}.txt", 'w') as f:
                                    f.writelines(mech_edit)'''

                                break
                            elif response.content.lower() == "stopcode":
                                await ctx.send("Command stopped.")
                                self.is_editing = False
                                done_flag = True  # Set the flag to True to exit the outer loop
                                break
                            else:
                                await ctx.send("Continuing with the current question.")
                                continue

                    if done_flag:
                        return

                    while not done_flag:
                        message = await ctx.send(
                            f"Type in some good **mech/pilot ability** you get from pilots that will be suitable for **{mech_name}**. Type **STOPCODE** to end the command or **SKIP** to skip this option.")

                        def check(msg):
                            return msg.author == ctx.author and msg.channel == ctx.channel

                        pilot_ability_msg = None
                        try:
                            pilot_ability_msg = await self.client.wait_for('message', check=check,
                                                                           timeout=editing_timer)
                        except asyncio.TimeoutError:
                            await ctx.send("You took too long to respond, command canceled.")
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break

                        if pilot_ability_msg.content.lower() == "stopcode":
                            await ctx.send("Command stopped.")
                            self.is_editing = False
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break
                        elif pilot_ability_msg.content.lower() == "skip":
                            mech_pilot_ability_line_index = -1
                            for i, line in enumerate(mech_edit):
                                if "Best Pilot Ability:" in line:
                                    mech_pilot_ability_line_index = i
                                    break

                            overall_approach_line_index = -1
                            for i, line in enumerate(mech_edit):
                                if "Overall Approach:" in line:
                                    overall_approach_line_index = i
                                    break

                            best_pilot_line = mech_edit[
                                              mech_pilot_ability_line_index + 1:overall_approach_line_index] if overall_approach_line_index > 0 else mech_edit[
                                                                                                                                                     mech_pilot_ability_line_index:]
                            self.responses_dict[arg]["pilot ability"] = "".join(best_pilot_line).strip()
                            break

                        else:
                            await ctx.send(
                                f"This is the description you gave for possible mech/pilot ability(s) for **{mech_name}**"
                                f"\nType **yes** to continue"
                                f"\nType **no** to continue editing"
                                f"\nType **stopcode** to end")

                            embed5 = disnake.Embed(title=f'{mech_name}: Pilot Abilities',
                                                    color=disnake.Color.from_rgb(100, 100, 100))
                            embed5.add_field(name="",
                                             value=f'{pilot_ability_msg.content}', inline=False)
                            embed5.set_footer(text=f'Page 5/7')
                            await ctx.send(embed=embed5)

                            def check_response(m):
                                return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in [
                                    'yes', 'no', 'stopcode']

                            try:
                                response = await self.client.wait_for('message', check=check_response,
                                                                      timeout=confirm_timer)
                            except asyncio.TimeoutError:
                                await ctx.send("You took too long to respond, command canceled.")
                                done_flag = True  # Set the flag to True to exit the outer loop
                                break

                            if response.content.lower() == "yes":
                                self.responses_dict[arg]["pilot ability"] = pilot_ability_msg.content

                                '''# Find the index where "Mech Pilot Ability:" and "Overall Approach:" section starts (if it exists)
                                for i, line in enumerate(mech_edit):
                                    if "Best Pilot Ability:" in line:
                                        mech_pilot_ability_line_index = i
                                    elif "Overall Approach:" in line:
                                        overall_approach_line_index = i
                                        break
                                # Remove the lines between "Mech Pilot Ability:" and "Overall Approach:"
                                if mech_pilot_ability_line_index != -1 and overall_approach_line_index != -1:
                                    del mech_edit[mech_pilot_ability_line_index + 1:overall_approach_line_index]

                                # Insert the new "Mech Pilot ability" section
                                mech_edit.insert(mech_pilot_ability_line_index + 1,f"\n{self.responses_dict[arg]['pilot ability']}\n\n")

                                # Write the updated content back to the file
                                with open(f"cogs/MechInfo/{mech_name}.txt", 'w') as f:
                                    f.writelines(mech_edit)'''

                                break
                            elif response.content.lower() == "stopcode":
                                await ctx.send("Command stopped.")
                                self.is_editing = False
                                done_flag = True  # Set the flag to True to exit the outer loop
                                break
                            else:
                                await ctx.send("Continuing with the current question.")
                                continue

                    if done_flag:
                        return

                    while not done_flag:
                        message = await ctx.send(
                            f"Type the **overall approach** when using  **{mech_name}**. Type **STOPCODE** to end the command or **SKIP** to skip this option.")

                        def check(msg):
                            return msg.author == ctx.author and msg.channel == ctx.channel

                        overall_approach_msg = None
                        try:
                            overall_approach_msg = await self.client.wait_for('message', check=check,
                                                                              timeout=editing_timer)
                        except asyncio.TimeoutError:
                            await ctx.send("You took too long to respond, command canceled.")
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break

                        if overall_approach_msg.content.lower() == "stopcode":
                            await ctx.send("Command stopped.")
                            self.is_editing = False
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break
                        elif overall_approach_msg.content.lower() == "skip":
                            for i, line in enumerate(mech_edit):
                                if "Overall Approach:" in line:
                                    overall_approach_line_index = i
                                    break

                            for i, line in enumerate(mech_edit):
                                if "Edited By:" in line:
                                    edit_arthurs_line_index = i
                                    break

                            overall_approach_line = mech_edit[
                                                    overall_approach_line_index + 1:edit_arthurs_line_index] if edit_arthurs_line_index > 0 else mech_edit[
                                                                                                                                                 overall_approach_line_index:]
                            self.responses_dict[arg]["overall approach"] = "".join(overall_approach_line).strip()

                            # Find the index where the "Background:" and "Weapons:" section starts (if it exists)
                            for i, line in enumerate(mech_edit):
                                if "Background:" in line:
                                    background_line_index = i
                                elif "Weapons:" in line:
                                    weapons_line_index = i
                                    break
                            # Remove the lines between "Background:" and "Weapons:"
                            if background_line_index != -1 and weapons_line_index != -1:
                                del mech_edit[background_line_index + 1:weapons_line_index]
                            # Insert the new "Background" section
                            mech_edit.insert(background_line_index + 1,
                                             f"\n{self.responses_dict[arg]['description']}\n\n")

                            # Find the index where the "Weapons:" and "Tactical Ability:" section starts (if it exists)
                            for i, line in enumerate(mech_edit):
                                if "Weapons:" in line:
                                    weapons_line_index = i
                                elif "Tactical Ability:" in line:
                                    tactical_ability_line_index = i
                                    break
                            # Remove the lines between "Background:" and "Weapons:"
                            if weapons_line_index != -1 and tactical_ability_line_index != -1:
                                del mech_edit[weapons_line_index + 1:tactical_ability_line_index]
                            # Insert the new "Weapons" section
                            mech_edit.insert(weapons_line_index + 1, f"\n{self.responses_dict[arg]['weapons']}\n\n")

                            # Find the index where the "Tactical Ability:" and "Builds:" section starts (if it exists)
                            for i, line in enumerate(mech_edit):
                                if "Tactical Ability:" in line:
                                    tactical_ability_line_index = i
                                elif "Builds:" in line:
                                    builds_line_index = i
                                    break
                            # Remove the lines between "Tactical Ability:" and "Builds:"
                            if tactical_ability_line_index != -1 and builds_line_index != -1:
                                del mech_edit[tactical_ability_line_index + 1:builds_line_index]
                            # Insert the new "Tactical Ability" section
                            mech_edit.insert(tactical_ability_line_index + 1,
                                             f"\n{self.responses_dict[arg]['tactical ability']}\n\n")

                            # Find the index where  "Builds:" and "Mech Pilot Ability:" section starts (if it exists)
                            for i, line in enumerate(mech_edit):
                                if "Builds:" in line:
                                    builds_line_index = i
                                elif "Best Pilot Ability:" in line:
                                    mech_pilot_ability_line_index = i
                                    break
                            # Remove the lines between "Builds:" and "Mech Pilot Ability:"
                            if builds_line_index != -1 and mech_pilot_ability_line_index != -1:
                                del mech_edit[builds_line_index + 1:mech_pilot_ability_line_index]
                            # Insert the new "Builds" section
                            mech_edit.insert(builds_line_index + 1, f"\n{self.responses_dict[arg]['build']}\n\n")

                            # Find the index where "Mech Pilot Ability:" and "Overall Approach:" section starts (if it exists)
                            for i, line in enumerate(mech_edit):
                                if "Best Pilot Ability:" in line:
                                    mech_pilot_ability_line_index = i
                                elif "Overall Approach:" in line:
                                    overall_approach_line_index = i
                                    break
                            # Remove the lines between "Mech Pilot Ability:" and "Overall Approach:"
                            if mech_pilot_ability_line_index != -1 and overall_approach_line_index != -1:
                                del mech_edit[mech_pilot_ability_line_index + 1:overall_approach_line_index]
                            # Insert the new "Mech Pilot ability" section
                            mech_edit.insert(mech_pilot_ability_line_index + 1,
                                             f"\n{self.responses_dict[arg]['pilot ability']}\n\n")

                            # Find the index where the "overall approch:" and "edited by::" section starts (if it exists)
                            for i, line in enumerate(mech_edit):
                                if "Overall Approach:" in line:
                                    overall_approach_line_index = i
                                elif "Edited By:" in line:
                                    edit_arthurs = i
                                    break
                            # Remove the lines between "overall approch::" and "edited by:::"
                            if overall_approach_line_index != -1 and edit_arthurs != -1:
                                del mech_edit[overall_approach_line_index + 1:edit_arthurs]
                            # Insert the new "Overall approach" section
                            mech_edit.insert(overall_approach_line_index + 1,
                                             f"\n{self.responses_dict[arg]['overall approach']}\n\n")

                            # Add the name of the user's name
                            mech_edit.insert(edit_arthurs + 1, f"{ctx.author}\n")

                            # Write the updated content back to the file
                            with open(f"cogs/MechInfo/{mech_name_all_lower}.txt", 'w') as f:
                                f.writelines(mech_edit)

                            await ctx.send(
                                f"Thank you for your suggestions, information on **{mech_name}** has been updated."
                                f"\nType **&mech {mech_name}** to see your changes.")

                            self.is_editing = False
                            done_flag = True  # Set the flag to True to exit the outer loop
                            break

                        else:
                            await ctx.send(
                                f"This is the description you gave for the overall approach for **{mech_name}**."
                                f"\nType **done** to submit your responses"
                                f"\nType **no** to continue editing"
                                f"\nType **stopcode** to end code"
                                f"\n---------------------"
                                f"\n{overall_approach_msg.content}"
                                f"\n---------------------")

                            embed6 = disnake.Embed(title=f'{mech_name}: Overall Approach',
                                                    color=disnake.Color.from_rgb(100, 100, 100))
                            embed6.add_field(name="",
                                             value=f'{overall_approach_msg.content}', inline=False)
                            embed6.set_footer(text=f'Page 6/7')
                            await ctx.send(embed=embed6)

                            def check_response(m):
                                return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in [
                                    'done', 'no', 'stopcode']

                            try:
                                response = await self.client.wait_for('message', check=check_response,
                                                                      timeout=confirm_timer)
                            except asyncio.TimeoutError:
                                await ctx.send("You took too long to respond, command canceled.")
                                done_flag = True  # Set the flag to True to exit the outer loop
                                break
                            finally:
                                self.is_editing = False

                            if response.content.lower() == "done":
                                self.responses_dict[arg]["overall approach"] = overall_approach_msg.content

                                # Find the index where the "Background:" and "Weapons:" section starts (if it exists)
                                for i, line in enumerate(mech_edit):
                                    if "Background:" in line:
                                        background_line_index = i
                                    elif "Weapons:" in line:
                                        weapons_line_index = i
                                        break
                                # Remove the lines between "Background:" and "Weapons:"
                                if background_line_index != -1 and weapons_line_index != -1:
                                    del mech_edit[background_line_index + 1:weapons_line_index]
                                # Insert the new "Background" section
                                mech_edit.insert(background_line_index + 1,
                                                 f"\n{self.responses_dict[arg]['description']}\n\n")

                                # Find the index where the "Weapons:" and "Tactical Ability:" section starts (if it exists)
                                for i, line in enumerate(mech_edit):
                                    if "Weapons:" in line:
                                        weapons_line_index = i
                                    elif "Tactical Ability:" in line:
                                        tactical_ability_line_index = i
                                        break
                                # Remove the lines between "Background:" and "Weapons:"
                                if weapons_line_index != -1 and tactical_ability_line_index != -1:
                                    del mech_edit[weapons_line_index + 1:tactical_ability_line_index]
                                # Insert the new "Weapons" section
                                mech_edit.insert(weapons_line_index + 1, f"\n{self.responses_dict[arg]['weapons']}\n\n")

                                # Find the index where the "Tactical Ability:" and "Builds:" section starts (if it exists)
                                for i, line in enumerate(mech_edit):
                                    if "Tactical Ability:" in line:
                                        tactical_ability_line_index = i
                                    elif "Builds:" in line:
                                        builds_line_index = i
                                        break
                                # Remove the lines between "Tactical Ability:" and "Builds:"
                                if tactical_ability_line_index != -1 and builds_line_index != -1:
                                    del mech_edit[tactical_ability_line_index + 1:builds_line_index]
                                # Insert the new "Tactical Ability" section
                                mech_edit.insert(tactical_ability_line_index + 1,
                                                 f"\n{self.responses_dict[arg]['tactical ability']}\n\n")

                                # Find the index where  "Builds:" and "Mech Pilot Ability:" section starts (if it exists)
                                for i, line in enumerate(mech_edit):
                                    if "Builds:" in line:
                                        builds_line_index = i
                                    elif "Best Pilot Ability:" in line:
                                        mech_pilot_ability_line_index = i
                                        break
                                # Remove the lines between "Builds:" and "Mech Pilot Ability:"
                                if builds_line_index != -1 and mech_pilot_ability_line_index != -1:
                                    del mech_edit[builds_line_index + 1:mech_pilot_ability_line_index]
                                # Insert the new "Builds" section
                                mech_edit.insert(builds_line_index + 1, f"\n{self.responses_dict[arg]['build']}\n\n")

                                # Find the index where "Mech Pilot Ability:" and "Overall Approach:" section starts (if it exists)
                                for i, line in enumerate(mech_edit):
                                    if "Best Pilot Ability:" in line:
                                        mech_pilot_ability_line_index = i
                                    elif "Overall Approach:" in line:
                                        overall_approach_line_index = i
                                        break
                                # Remove the lines between "Mech Pilot Ability:" and "Overall Approach:"
                                if mech_pilot_ability_line_index != -1 and overall_approach_line_index != -1:
                                    del mech_edit[mech_pilot_ability_line_index + 1:overall_approach_line_index]
                                # Insert the new "Mech Pilot ability" section
                                mech_edit.insert(mech_pilot_ability_line_index + 1,
                                                 f"\n{self.responses_dict[arg]['pilot ability']}\n\n")

                                # Find the index where the "overall approch:" and "edited by::" section starts (if it exists)
                                for i, line in enumerate(mech_edit):
                                    if "Overall Approach:" in line:
                                        overall_approach_line_index = i
                                    elif "Edited By:" in line:
                                        edit_arthurs = i
                                        break
                                # Remove the lines between "overall approch::" and "edited by:::"
                                if overall_approach_line_index != -1 and edit_arthurs != -1:
                                    del mech_edit[overall_approach_line_index + 1:edit_arthurs]
                                # Insert the new "Overall approach" section
                                mech_edit.insert(overall_approach_line_index + 1,
                                                 f"\n{self.responses_dict[arg]['overall approach']}\n\n")

                                # Add the name of the user's name
                                mech_edit.insert(edit_arthurs + 1, f"{ctx.author}\n")

                                # Write the updated content back to the file
                                with open(f"cogs/MechInfo/{mech_name_all_lower}.txt", 'w') as f:
                                    f.writelines(mech_edit)

                                self.responses_dict[arg]["overall_approach"] = overall_approach_msg.content

                                await ctx.send(
                                    f"Thank you for your suggestions, information on **{mech_name}** has been updated."
                                    f"\nType **&mech {mech_name}** to see your changes.")
                                self.is_editing = False
                                break
                            elif response.content.lower() == "stopcode":
                                await ctx.send("Command stopped.")
                                self.is_editing = False
                                done_flag = True  # Set the flag to True to exit the outer loop
                                break
                            else:
                                await ctx.send("Continuing with the current question.")
                                continue
                    if done_flag:
                        return


                elif reaction is not None and str(reaction.emoji) == '❌':
                    await ctx.send("canceled")


            else:
                await ctx.send(f"{arg} is not a mech or isn't read yet.")

        except Exception as error:
            print(f"{error}")
            await ctx.send(f"Problem: **[{error}]**")
        finally:
            self.is_editing = False

    # print(self.responses_dict) #will print all the entries
    # print(self.responses_dict[arg]["weapons"])  # will print entry for weapons
    # print(self.responses_dict[arg]["description"])
    # print(self.responses_dict[arg]["pilot ability"])

    @commands.command()
    async def send(self, ctx):
        message = await ctx.send('hmm…')
        message_id = message.id
        await ctx.send(message_id)

    @commands.command()
    async def image(self, ctx):
        await ctx.send(file=disnake.File('images/mech/TrioDemech.jpg'))

        # MEH


def setup(client):
    client.add_cog(mech(client))  # bot.add_cog(mech(bot)) is the name of the cog "mech" must match line 8