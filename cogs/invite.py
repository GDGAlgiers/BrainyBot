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
    async def invite(self, context, member: discord.Member):
        author = context.author
        currentChannel = context.channel
        currentCategory = currentChannel.category

        if (currentCategory.name == config.CATEGORY_FOR_INVITATION):
            channels = author.guild.channels

            team_channels = filter(
                lambda channel: channel.name.startswith(
                    config.TEAM_WORKSPACE_PREFIX) == True and channel.
                permissions_for(author).read_messages == True, channels)

            for team in team_channels:
                await currentChannel.send("{} is a member in {}".format(
                    author.name, team.mention))
                
                overwrite = discord.PermissionOverwrite(
                    read_messages=True,
                    read_message_history=True,
                    send_messages=True,
                    embed_links=True,
                    attach_files=True,
                    add_reactions=True,
                )
                await team.set_permissions(member, overwrite=overwrite)

                await team.send("walcome {}".format(member.mention))

            await currentChannel.send("inviting {}".format(member.mention))


def setup(bot):
    bot.add_cog(Invite(bot))
