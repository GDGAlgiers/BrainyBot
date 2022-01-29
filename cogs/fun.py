"""
    This is where we will have most of the fun commands 
"""
import os
import sys
import random
import json
import csv
import discord
from discord.ext import commands
from core.utils import loads_to_object


if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    config = loads_to_object("config.json")


class Fun(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Tweet as someone", description='You can tweet as someone else to troll others')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def tweet(self, ctx, username: commands.clean_content(fix_channel_mentions=True), *, text: commands.clean_content(fix_channel_mentions=True)):
        """ Tweet as someone else.
            $tweet @user text
         """

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
        with open("core/BrainyAdvice.csv", 'r') as dataset:
            advices_list = list(csv.reader(dataset, delimiter=','))
            advices_len = len(advices_list)
            number = random.randint(0,advices_len)
            advice = advices_list[number][0]
            await ctx.send(advice)

    @commands.command(
        brief="Get a Quote",
        description="Get an inspirational quote from a wise bot :) ",
    )
    async def quote(self, ctx):
        """Get an inspirational quote from a wise bot :)"""

        await ctx.trigger_typing()
        # Quotes based on https://gist.github.com/JakubPetriska/060958fd744ca34f099e947cd080b540
        with open("core/BrainyQuotes.csv", "r") as dataset:
            quotes_list = list(csv.reader(dataset, delimiter=","))
            quotes_len = len(quotes_list)
            number = random.randint(0, quotes_len - 1)
            author, quote = quotes_list[number]
            if not author:
                author = "Someone"
            await ctx.send(f"{author}: {quote}")


def setup(bot):
    bot.add_cog(Fun(bot))
