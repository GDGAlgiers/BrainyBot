"""
    This is where we will put all our hashcode commands
"""
import os
import datetime
import sys
import discord
from discord.ext import commands
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config



class hashcode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    # get the time left to end of the hashcode
    # TODO: change hard coded start time
    start_time = datetime.datetime(2021, 2, 25, 17, 0, 0, 0)
    duration = datetime.timedelta(hours=4)
    end = start_time + duration

    @commands.command(description="Get the time left to the end of the competition")
    async def timeLeft(self, ctx):
        now = datetime.datetime.now()
        delta = self.end - now
        hours_left = delta.seconds // 3600
        minutes_left = (delta.seconds % 3600) // 60
        seconds_left = (delta.seconds % 3600 ) % 60
        await ctx.message.channel.send(f"Time left {hours_left}hours {minutes_left}minutes {seconds_left}seconds")
    


def setup(bot):
    bot.add_cog(hashcode(bot))
