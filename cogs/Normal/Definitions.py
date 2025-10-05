from disnake.ext import commands
import traceback
from PyDictionary import PyDictionary
dictionary = PyDictionary()

class Definition(commands.Cog):
    def __init__(self, client):
        self.client = client

    # SMC STUFF

    @commands.command()
    async def d(self, ctx, *args):
        num_arg = len(args)

        try:
            if num_arg == 1:
                # print(f"Arg: {args[0]}")
                word = args[0]
                if word.isalpha():
                    meaning = dictionary.meaning(word)
                    if meaning[0] is None:
                        await ctx.send(f"Unable to find a definition for {word}")
                    else:
                        await ctx.send(f"Printing {word}")
                        await ctx.send(meaning)
                else:
                    await ctx.send(f"Must contain only letters {args[0]}")
                return
            elif num_arg == 2:
                print(f"Arg: {args[1]}")
                word = args[1]
                if word.isalpha():
                    await ctx.send(word)
                else:
                    await ctx.send(f"Must contain only letters {args[1]}")
                return
        except Exception as error:
            error_info = traceback.format_exc()
            await ctx.send(f"Error: {error}")
            print(f"Error: {error}\n{error_info}")
            return


def setup(client):
    client.add_cog(Definition(client))    # bot.add_cog(mech(bot)) is the name of the cog "mech" must match line 8