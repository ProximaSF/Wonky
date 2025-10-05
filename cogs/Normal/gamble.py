import random
import disnake
from disnake.ext import commands

from cogs.System.PointsAdjust import Adjust_WobbleBBits

Instance_WobbleBits = Adjust_WobbleBBits()



class gamble(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def flip(self, ctx, *args):
        flip = ["H", "T"]
        flip_winner = random.choice(flip)
        num_args = len(args)
        # print(num_args)

        if num_args == 1:
            # print("lol")
            for arg in args:
                if "H" in arg or "h" in arg:
                    if flip_winner == "H":
                        file = disnake.File("images/coin_head.png")
                        embed = disnake.Embed(title=f"{ctx.author.name}: Nice, You landed a **head**!",
                                              color=disnake.Color.orange())
                        embed.set_image(url="attachment://coin_head.png")
                        await ctx.send(embed=embed, file=file)
                    else:
                        file = disnake.File("images/coin_tail.png")
                        embed = disnake.Embed(title=f"{ctx.author.name}: Aw, you landed a **tail**!",
                                              color=disnake.Color.orange())
                        embed.set_image(url="attachment://coin_tail.png")
                        await ctx.send(embed=embed, file=file)
                elif "T" in arg or "t" in arg:
                    if flip_winner == "T":
                        file = disnake.File("images/coin_tail.png")
                        embed = disnake.Embed(title=f"{ctx.author.name}: Nice, you landed a **tail**!",
                                              color=disnake.Color.orange())
                        embed.set_image(url="attachment://coin_tail.png")
                        await ctx.send(embed=embed, file=file)
                    else:
                        file = disnake.File("images/coin_head.png")
                        embed = disnake.Embed(title=f"{ctx.author.name}: Aw, you landed a **head**!",
                                              color=disnake.Color.orange())
                        embed.set_image(url="attachment://coin_head.png")
                        await ctx.send(embed=embed, file=file)
                else:
                    await ctx.send(f"Type **H** or **T** after &flip. Enter a value after h/t to gaamble.")
        if num_args == 2:
            arg1 = args[0]
            arg2 = args[1]
            total_WobbleBits = int(arg2)
            # print(total_WobbleBits)
            if arg1 in ['h', 'H', 't', 'T'] and arg2.isdigit():
                if arg1 in ['H', 'h']:
                    if Instance_WobbleBits.get_WobbleBits(ctx.author.id) >= total_WobbleBits:
                        if flip_winner == "H":
                            file = disnake.File("images/coin_head.png")
                            embed = disnake.Embed(
                                title=f"{ctx.author.name}: Nice, You landed a **head**! You earned **{total_WobbleBits}** WobbleBits!",
                                color=disnake.Color.orange())
                            embed.set_image(url="attachment://coin_head.png")
                            await ctx.send(embed=embed, file=file)
                            Instance_WobbleBits.add_WobbleBits(ctx.author.id, total_WobbleBits)
                        else:
                            file = disnake.File("images/coin_tail.png")
                            embed = disnake.Embed(
                                title=f"{ctx.author.name}: Aw, you landed a **tail**! You lost **{total_WobbleBits}** WobbleBits!",
                                color=disnake.Color.orange())
                            embed.set_image(url="attachment://coin_tail.png")
                            await ctx.send(embed=embed, file=file)
                            Instance_WobbleBits.sub_WobbleBits(ctx.author.id, total_WobbleBits)
                    else:
                        # user doesn't have enough WobbleBits, display error message
                        await ctx.send(
                            f"Sorry, you don't have enough WobbleBits to place that bet. You only have **{Instance_WobbleBits.get_WobbleBits(ctx.author.id)}** WobbleBits ")

                elif arg1 in ['T', 't']:
                    if Instance_WobbleBits.get_WobbleBits(ctx.author.id) >= total_WobbleBits:
                        if flip_winner == "T":
                            file = disnake.File("images/coin_tail.png")
                            embed = disnake.Embed(
                                title=f"{ctx.author.name}: Nice, you landed a **tail**! You earned **{total_WobbleBits}** WobbleBits!",
                                color=disnake.Color.orange())
                            embed.set_image(url="attachment://coin_tail.png")
                            await ctx.send(embed=embed, file=file)
                            Instance_WobbleBits.add_WobbleBits(ctx.author.id, total_WobbleBits)
                        else:
                            file = disnake.File("images/coin_head.png")
                            embed = disnake.Embed(
                                title=f"{ctx.author.name}: Aw, you landed a **head**! You lost **{total_WobbleBits}** WobbleBits!",
                                color=disnake.Color.orange())
                            embed.set_image(url="attachment://coin_head.png")
                            await ctx.send(embed=embed, file=file)
                            Instance_WobbleBits.sub_WobbleBits(ctx.author.id, total_WobbleBits)
                    else:
                        # user doesn't have enough WobbleBits, display error message
                        await ctx.send(
                            f"Sorry, you don't have enough WobbleBits to place that bet. You only have **{Instance_WobbleBits.get_WobbleBits(ctx.author.id)}** WobbleBits ")
            else:
                await ctx.send('Invalid arguments. Enter an **h**/**t** followed by a number if you want to bet.')

    @commands.command()
    async def steal(self, ctx, *args):
        num_args = len(args)
        if num_args == 1:
            try:
                # print(get_steal_attempts(ctx.author.id))

                value = int(args[0])
                total_WobbleBits = value

                # print(f"{value} \n {type(value)}")
                members = ctx.guild.members
                members.remove(ctx.author)
                randomMember = random.choice(members)

                ran_chance_steal = random.random()
                # print(f"ran_chance_steal: {ran_chance_steal}")
                # print(randomMember.id)
                # print(f"user ID: {ctx.author.id}")
                while True:
                    if total_WobbleBits > 50:
                        await ctx.send("Max steal is 50")
                        break
                    else:

                        if Instance_WobbleBits.get_steal_attempts(ctx.author.id) == 0:
                            await ctx.send(f"You ran out of steal attempts, comeback in 12 hours to try again")
                            break
                        # print(type(Instance_WobbleBits.get_WobbleBits(ctx.author.id))

                        eligible_members = [member for member in members if
                                            Instance_WobbleBits.get_WobbleBits(member.id) is not None and
                                            Instance_WobbleBits.get_WobbleBits(member.id) >= total_WobbleBits and
                                            Instance_WobbleBits.get_WobbleBits(ctx.author.id) >= 0]

                        # await ctx.send(eligible_members)

                        if not eligible_members:
                            await ctx.send(
                                f"Unable to steal: you're either broke or there isn't a member that have {value} WobbleBits.")
                            break

                        randomMember = random.choice(eligible_members)
                        # print(randomMember)

                        if ran_chance_steal <= 0.1:
                            await ctx.send(
                                f'**{ctx.author.name}** manage to steal **{value}** WobbleBits from **{randomMember.name}** without getting caught! [{Instance_WobbleBits.get_steal_attempts(ctx.author.id) - 1} steals left].')
                            # print(randomMember.id)
                            Instance_WobbleBits.sub_WobbleBits(randomMember.id, total_WobbleBits)
                            Instance_WobbleBits.add_WobbleBits(ctx.author.id, total_WobbleBits)
                            Instance_WobbleBits.sub_steal_attempts(ctx.author.id, 1)
                            break

                        elif ran_chance_steal <= 0.4:
                            ran_chance_consequence = random.random()
                            chance_consequence = 0.5
                            if ran_chance_consequence <= chance_consequence:
                                ran_WobbleBits_sue = random.randint(20, 20 + value // 1.5)
                                # print(f"sued for {ran_WobbleBits_sue}")
                                await ctx.send(
                                    f'**{ctx.author.name}** was caught stealing WobbleBits from **{randomMember.name}** and was sued for {ran_WobbleBits_sue} WobbleBits. [{Instance_WobbleBits.get_steal_attempts(ctx.author.id) - 1} steals left].')
                                Instance_WobbleBits.sub_WobbleBits(ctx.author.id, ran_WobbleBits_sue)
                                Instance_WobbleBits.add_WobbleBits(randomMember.id, ran_WobbleBits_sue)
                                Instance_WobbleBits.sub_steal_attempts(ctx.author.id, 1)
                                break
                            else:
                                await ctx.send(
                                    f'**{ctx.author.name}** was caught stealing WobbleBits from **{randomMember.name}** but manage to run away. [{Instance_WobbleBits.get_steal_attempts(ctx.author.id) - 1} steals left].')
                                Instance_WobbleBits.sub_steal_attempts(ctx.author.id, 1)
                                break

                        else:
                            ran_WobbleBits_steal = random.randint(1, value)
                            # print(ran_WobbleBits_steal)
                            await ctx.send(
                                f'**{ctx.author.name}** only manage to steal **{ran_WobbleBits_steal}** WobbleBits from **{randomMember.name}** without getting caught. [{Instance_WobbleBits.get_steal_attempts(ctx.author.id) - 1} steals left].')
                            Instance_WobbleBits.sub_WobbleBits(randomMember.id, ran_WobbleBits_steal)
                            Instance_WobbleBits.add_WobbleBits(ctx.author.id, ran_WobbleBits_steal)
                            Instance_WobbleBits.sub_steal_attempts(ctx.author.id, 1)
                            break
            except ValueError:
                await ctx.send("Invalid value. Please provide a valid integer to steal from a random member.")

        elif num_args == 2:
            #print("works")
            try:
                def sub_health(user_id, health):
                    user = disnake.utils.get(ctx.guild.members, id=int(user_id))
                    if user.bot:
                        return  # If user is a bot, return without adding WobbleBits

                    with open("txt/playerpoints.txt", "r+") as f:
                        lines = f.readlines()
                        f.seek(0)
                        user_found = False
                        for i, line in enumerate(lines):
                            if line.startswith(f"[{user_id}]: "):
                                user_found = True

                                health_line = lines[i + 2]
                                current_health = int(health_line.strip().split(': ')[1])
                                new_health = current_health - health
                                # print(current_WobbleBits)
                                lines[i + 2] = f"\tHealth: {new_health}\n"
                                break
                        f.seek(0)
                        f.writelines(lines)
                        f.truncate()

                member = await commands.MemberConverter().convert(ctx, args[0])
                value = int(args[1])
                total_WobbleBits = value

                members = ctx.guild.members
                members.remove(ctx.author)

                ran_chance_steal = random.random()
                # print(f"ran_chance_steal: {ran_chance_steal}")
                print(f"user ID: {ctx.author.id}")

                while True:
                    if Instance_WobbleBits.get_steal_attempts(ctx.author.id) == 0:
                        await ctx.send(f"You ran out of steal attempts, comeback in 12 hours to try again")
                        break
                    if member is ctx.author:
                        selfkidnap = ["Trying to steal your own money...?",
                                      f"Bruh, someone steal money from {ctx.author.name}",
                                      "yeah, it doesn't work like that :|"]
                        random_selfsteal = random.choice(selfkidnap)
                        await ctx.send(random_selfsteal)
                        break
                    eligible_members = [member for member in members if
                                        Instance_WobbleBits.get_WobbleBits(member.id) is not None and
                                        Instance_WobbleBits.get_WobbleBits(member.id) >= total_WobbleBits and
                                        Instance_WobbleBits.get_WobbleBits(ctx.author.id) >= 0]
                    if member.bot:
                        await ctx.send("You can't steal from a bot, pick a user within the server")
                        break
                    if not eligible_members:
                        await ctx.send(
                            f"Unable to steal: you're either have negative bits or there isn't a member that's worth {value} WobbleBits.")
                        break

                    else:

                        # 10% steal all of it without getting caught
                        if ran_chance_steal <= 0.1:
                            await ctx.send(
                                f'**{ctx.author.name}** manage to steal the full amount (**{value}** WobbleBits) from **{member.name}** without getting caught! [{Instance_WobbleBits.get_steal_attempts(ctx.author.id) - 1} steals left].')
                            # print(randomMember.id)
                            Instance_WobbleBits.sub_WobbleBits(member.id, total_WobbleBits)
                            Instance_WobbleBits.add_WobbleBits(ctx.author.id, total_WobbleBits)
                            Instance_WobbleBits.sub_steal_attempts(ctx.author.id, 1)
                            break

                        # 40% getting caught
                        elif ran_chance_steal <= 0.4:
                            ran_chance_consequence = random.random()

                            # 40% getting sued
                            if ran_chance_consequence <= 0.4:
                                ran_WobbleBits_sue = random.randint(20, 20 + value // 1.5)
                                # print(f"sued for {ran_WobbleBits_sue}")
                                await ctx.send(
                                    f'**{ctx.author.name}** was caught stealing WobbleBits from **{member.name}** and was sued for {ran_WobbleBits_sue} WobbleBits. [{Instance_WobbleBits.get_steal_attempts(ctx.author.id) - 1} steals left].')
                                Instance_WobbleBits.sub_WobbleBits(ctx.author.id, ran_WobbleBits_sue)
                                Instance_WobbleBits.add_WobbleBits(member.id, ran_WobbleBits_sue)
                                Instance_WobbleBits.sub_steal_attempts(ctx.author.id, 1)
                                break

                            # 40% getting hurt
                            if ran_chance_consequence <= 0.8:
                                health_lost_chance = random.random()

                                health_lost_minor = random.randint(1, 5)
                                health_lost_medium = random.randint(5, 15)
                                health_lost_major = random.randint(15, 50)

                                if health_lost_chance <= 1.0:
                                    await ctx.send(
                                        f'**{ctx.author.name}** was caught stealing from **{member.name}\'** guard dog and was attacked, loosing {health_lost_minor} hit-points. [{Instance_WobbleBits.get_steal_attempts(ctx.author.id) - 1} steals left].')
                                    Instance_WobbleBits.sub_steal_attempts(ctx.author.id, 1)
                                    sub_health(ctx.author.id, health_lost_minor)
                                    break

                                if health_lost_chance <= 0.5:
                                    await ctx.send(
                                        f'**{ctx.author.name}** was caught stealing from **{member.name}\'** guard dog and was attacked, loosing {health_lost_medium} hit-points. [{Instance_WobbleBits.get_steal_attempts(ctx.author.id) - 1} steals left].')
                                    Instance_WobbleBits.sub_steal_attempts(ctx.author.id, 1)
                                    sub_health(ctx.author.id, health_lost_medium)
                                    break

                                if health_lost_chance <= 0.2:
                                    await ctx.send(
                                        f'**{ctx.author.name}** was caught stealing from **{member.name}\'** guard dog and was attacked, loosing {health_lost_major} hit-points. [{Instance_WobbleBits.get_steal_attempts(ctx.author.id) - 1} steals left].')
                                    Instance_WobbleBits.sub_steal_attempts(ctx.author.id, 1)
                                    sub_health(ctx.author.id, health_lost_major)
                                    break

                            # 20% getting nothing
                            else:
                                await ctx.send(
                                    f'**{ctx.author.name}** was caught stealing WobbleBits from **{member.name}** but manage to run away. [{Instance_WobbleBits.get_steal_attempts(ctx.author.id) - 1} steals left].')
                                Instance_WobbleBits.sub_steal_attempts(ctx.author.id, 1)
                                break

                        else:
                            ran_WobbleBits_steal = random.randint(1, value)
                            # print(ran_WobbleBits_steal)
                            await ctx.send(
                                f'**{ctx.author.name}** only manage to steal **{ran_WobbleBits_steal}** WobbleBits from **{member.name}** without getting caught. [{Instance_WobbleBits.get_steal_attempts(ctx.author.id) - 1} steals left].')
                            Instance_WobbleBits.sub_WobbleBits(member.id, ran_WobbleBits_steal)
                            Instance_WobbleBits.add_WobbleBits(ctx.author.id, ran_WobbleBits_steal)
                            Instance_WobbleBits.sub_steal_attempts(ctx.author.id, 1)
                            break
                        await ctx.send(f"{ctx.author.name} tried to steal {value} from {member.name}")
                        break
            except ValueError:
                await ctx.send("Invalid inputs. Please provide the @user than the amount you think you can steal.")


def setup(client):
    client.add_cog(gamble(client))