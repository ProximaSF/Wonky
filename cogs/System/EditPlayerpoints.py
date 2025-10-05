from disnake.ext import commands
import asyncio


class EditPlayerpoints(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.last_item = None  # initialize self.last_item to None
        self.picked_item = None

    @commands.has_any_role("Admin")
    @commands.command()  # Used to determine where you want the new item to be added within the item list in playerpoints.txt.
    async def pick2402(self, ctx):
        await ctx.send(f"Which item (existing) do you want the new item to be under when you use **addpick**?")
        msg = await self.client.wait_for('message')

        await asyncio.sleep(1)

        with open("cogs/txt/playerpoints.txt", 'r') as f:
            lines = f.readlines()

        for line in lines:
            if msg.content in line:
                self.picked_item = line.split(":")[0].strip()  # update self.picked_item if a new item is found
                await ctx.send(
                    f"{msg.content} has been set. Use **pick2402** again to reset and pick another existing item.")
                return
            else:
                continue

    @commands.has_any_role("Admin")
    @commands.command()  # used to add new items in the playerpoints.txt at the bottom if pick2402 command was not used. Else it will add the new
    # item beneath the called item used in pick2402
    async def addpick(self, ctx):
        if self.picked_item is None:
            await ctx.send(
                "You have to used **pick2402** first. If you want to add a item under an existing item, use **pick2402**.")
            raise ValueError("self.picked_item cannot be None")

        await ctx.send(f"What item do you want to add?")
        msg = await self.client.wait_for('message')

        with open("txt/playerpoints.txt", 'r') as f:
            lines = f.readlines()

        with open("txt/playerpoints.txt", 'w') as f:
            for line in lines:
                if self.picked_item in line:
                    line = line.rstrip('\n') + f"\n\t{msg.content}: 0\n"
                f.write(line)
            self.picked_item = None
            await ctx.send(f"{msg.content} has been added as an item. Use **pick2402** to use this command again.")

    @commands.has_any_role("Admin")
    @commands.command()  # will call the last item in the list in the file playerpoint.txt so addlast can be used
    async def last2402(self, ctx):
        with open("txt/playerpoints.txt", 'r') as f:
            lines = f.readlines()

        for line in lines:
            if ":" in line:
                self.last_item = line.split(":")[0].strip()  # update self.last_item if a new item is found
            elif '[' in line and ']' in line:
                pass  # reset self.last_item when a new user is found
            else:
                continue  # ignore other lines
        await ctx.send(f"Last item is **{self.last_item}**")

    @commands.has_any_role("Admin")
    @commands.command()  # can be used once last2402 have been used
    async def addlast(self, ctx):
        if self.last_item is None:
            await ctx.send(f"Use **last2402** first to get the last item in the list")
            raise ValueError("self.picked_item cannot be None")

        await ctx.send(f"What item do you want to add at the end of the list?")
        msg = await self.client.wait_for('message')

        with open("txt/playerpoints.txt", 'r') as f:
            lines = f.readlines()

        with open("txt/playerpoints.txt", 'w') as f:
            for line in lines:
                if self.last_item in line:
                    line = line.rstrip('\n') + f"\n\t{msg.content}: 0\n"
                f.write(line)
            await ctx.send(f"{msg.content} has been added. Use **last2402**  to use this command again.")
            self.last_item = None

    @commands.has_any_role("Admin")
    @commands.command()  # will remove any (existing) item in the list for playerpoint.txt
    async def removeitem(self, ctx):
        await ctx.send(f"What item do you want to remove?")
        await asyncio.sleep(1)
        msg = await self.client.wait_for('message')
        item_to_remove = msg.content

        with open("txt/playerpoints.txt", 'r') as f:
            lines = f.readlines()

        with open("txt/playerpoints.txt", 'w') as f:
            for line in lines:
                if item_to_remove in line:
                    continue  # skip the line that contains the item to remove
                f.write(line)
            await ctx.send(f"**{item_to_remove}** has been removed")

    @commands.has_any_role("Admin")
    @commands.command()  # Used to remove and replace point on a existing item
    async def replacepoints(self, ctx):
        await ctx.send(
            f"What item do you want to change points? Will affect all user! Use the right word(s) found in the txt file for playerpoints.txt")
        msg = await self.client.wait_for('message')
        item_change_name = msg.content
        await asyncio.sleep(1)
        await ctx.send(f"What value do you want to change to? Will affect all user!")
        msg = await self.client.wait_for('message')
        item_change_value = msg.content

        with open("txt/playerpoints.txt", 'r') as f:
            lines = f.readlines()
        found_item = False

        with open("txt/playerpoints.txt", 'w') as f:
            for line in lines:
                if item_change_name in line:
                    line = f"\t{item_change_name}: {int(item_change_value)}\n"
                    found_item = True
                f.write(line)

            if not found_item:
                await ctx.send(f"Use a existing item")


def setup(client):
    client.add_cog(EditPlayerpoints(client))
