import asyncio
import ntpath
import random
import time
import datetime
from datetime import datetime
import disnake
from disnake.ext import commands
from dotenv import load_dotenv
from disnake.ext.commands import check

import os
from os import getenv
import re
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint

from PIL import Image
from io import BytesIO

class SMC(commands.Cog):
    def __init__(self, client):
        self.client = client

    # SMC STUFF

    @commands.command()
    async def challenge(self, ctx):
        lol = ["👀", "🤷.", "good luck 👍!", "sounds easy enough", "send a SS of how you did."]
        lol_picker = random.choice(lol)
        randomMember = random.choice(ctx.guild.members)

        pilots = ["Ning", "Rom", "Jonna", "Vita", "Jiu Chong", "Ivan", "Lori", "Mila", "R.E.D", "Lillian",
                         "Kizuna AI", "Silver Deacon",
                         "Cyrus", "Serena", "Norma", "Yutong", "Nighthawk", "Mobius", "Shin", "Zoe", "Purity", "Jaka",
                         "Riko - Yaheeee"]

        random_pilots = random.choice(pilots)

        second_veb = ["with a core you usually don't use",
                      "on 30 fps", "with sensitivity 1.5x higher what you're using",
                      "in TDM without a team", "in squad but solo", f"with **{randomMember.display_name}**",
                      "with gyroscope enabled, if already invert your x-axs", "with gyroscope enabled, if already invert your y-axs",
                      "with a clan mate", f"while using {random_pilots} with mech talent you don't use", f"while using {random_pilots} until you win a match",
                      f"while using {random_pilots}",
                      "with a BR player but in TDM", "with a TDM player but in BR", "on a different server", "using two fingers if you're using more than 2 already"
                      "and score an average damage of 40k+ in a TDM match", "and score an average damage of 60k+ in a TDM match",
                      "and turn off gyro for 3 match if it's on"]

        second_veb_random = random.choice(second_veb)

        mech = ["Arthur", "Snow", "Hotsteel", "Raven", "Gabriel", "Pulsar", "Michael", "Hurricane", "Boltus",
                "Ranger", "Firefox", "Firestar", "Aurora", "Caramel", "Trio", "Skylark", "Andromeda",
                "Doomlight", "Ventorus", "Northern Knight", "Flamenco", "Neutron", "Alborada", "Jojo", "Skyfall",
                "Akashic", "Dreadwolf", "Death Knell", "Moon Rabbit", "Pulsar", "Raven", 'Tempest', "Neutron",
                "Northern Knight", "Pulsar", "Guerilla Hunter", "Gabriel"]

        mech_picker = random.choice(mech)
        mech_picker_two = random.choice(mech)
        if mech_picker == mech_picker_two:
            mech.remove(mech_picker_two)
            mech_picker_three = random.choice()
            await ctx.channel.send(
                f"> {ctx.author.mention}, play **{mech_picker}** or **{mech_picker_three}** {second_veb_random} - {lol_picker}")
        else:
            await ctx.channel.send(
                f"> {ctx.author.mention}, play **{mech_picker}** or **{mech_picker_two}** {second_veb_random} - {lol_picker}")

    @commands.command()
    async def v4vxv(self, ctx):
        randomMember = random.choice(ctx.guild.members)
        v4vxv = ["is holding a heart.", "cut up a pp (ping pong).", "is probably an emu.",
                 "is going to pop you with his 2019 Nerf Ultra One Motorized Blaster!",
                 f"is going to smash either you or {randomMember.mention} 👀:", "is finally not playing Ventorus!",
                 "is simping for you 😉",
                 "decided to main Snow because ProximaSF and Bright said so.",
                 f"stole {randomMember.mention}'s swag - GOD DAMN!", "decided to become the new saviour",
                 "be carrying too much",
                 "mom is hotter than yours 🔥",
                 f"solved the question 'where is Waldo?'... in {randomMember.mention}'s 2021 Hunda Ultra Delux SUV Hatchback"]
        v4vxv_picker = random.choice(v4vxv)
        await ctx.send(f'v4 {v4vxv_picker}')


def setup(client):
    client.add_cog(SMC(client))   #bot.add_cog(mech(bot)) is the name of the cog "mech" must match line 8