import os
import sys
import discord
from discord.ext import commands
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


class Invite(commands.Cog, name="invite"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invite")
    async def invite(self, context, member:discord.Member):
      currentChannel = context.channel;
      
      if(currentChannel.name == config.INVITATION_CHANNEL_NAME):
        await currentChannel.send("inviting {}".format(member.mention));


def setup(bot):
    bot.add_cog(Invite(bot))
