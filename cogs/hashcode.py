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
    # TODO: remove hard coded start time
    start_time = datetime.datetime(2021, 2, 25, 17, 0, 0, 0)
    duration = datetime.timedelta(hours=4)
    end = start_time + duration

    @commands.command()
    async def timeLeft(self, ctx):
        now = datetime.datetime.now()
        delta = end - now
        hours_left = delta.seconds // 3600
        minutes_left = (delta.seconds % 3600) // 60
        seconds_left = (delta.seconds % 3600 ) % 60
        await ctx.send(f"Time left {hours_left}hours {minutes_left}minutes {seconds_left}seconds")
    
    # post a message by the moderator to a specified channel
    @commands.command()
    async def post(ctx, channel_name, *, message=None):
        author = ctx.message.author
        if "botmoderator" in [y.name.lower() for y in author.roles]:
            channel_obj = discord.utils.get(ctx.guild.channels, name=channel_name)
            if channel_obj:
                channel_id = channel_obj.id
                channel = bot.get_channel(channel_id)
                await channel.send(message)
            else:
                await ctx.send(f":weary: channel {channel_name} does not exist")




def setup(bot):
    bot.add_cog(hashcode(bot))
