"""
    This is where we will have most of the fun commands 
"""
import os
import sys
import json
import discord
from discord.ext import commands
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Tweet as someone", description='You can tweet as someone else to troll others')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tweet(self, ctx, username: commands.clean_content(fix_channel_mentions=True), *, text: commands.clean_content(fix_channel_mentions=True)):
        """ Tweet as someone else. """

        if len(text) > 65:
            text = text[:65]
            text += "..."

        await ctx.trigger_typing()
        async with self.bot.session.get("https://nekobot.xyz/api/imagegen?type=tweet&username={}&text={}".format(username, text)) as r:
            res = await r.json()

        embed = discord.Embed(color=0x00FF00,
                              title=f"You made {username} tweet this:")
        embed.set_image(url=res["message"])
        await ctx.send(embed=embed)

    @commands.command(brief="Get an Advice", description='Get an advice from a wise bot :) ')
    async def advice(self, ctx):
        """Get an advice from a wise bot :) """

        await ctx.trigger_typing()
        async with self.bot.session.get("https://api.adviceslip.com/advice") as r:
            res = await r.text()
        json_res = json.loads(res)
        await ctx.send(json_res["slip"]["advice"])


def setup(bot):
    bot.add_cog(Fun(bot))
