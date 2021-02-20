import os
import sys
import discord
from discord.ext import commands
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


def Auth(uuid):
    # todo implement the auth function
    return True, "test"


class Invite(commands.Cog, name="invite"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invite")
    async def invite(self, context, member: discord.Member):

        author = context.author
        currentChannel = context.channel
        currentCategory = currentChannel.category

        exists, teamName = Auth(author.id)

        if (exists and currentCategory.name == f"{teamName}_category"):

            team_category = currentCategory
            #team_channels = team_category.channels

            overwrite = discord.PermissionOverwrite(view_channel=True,
                                                    read_messages=True,
                                                    read_message_history=True,
                                                    send_messages=True,
                                                    embed_links=True,
                                                    attach_files=True,
                                                    add_reactions=True,
                                                    connect=True,
                                                    speak=True,
                                                    stream=True)

            await team_category.set_permissions(member, overwrite=overwrite)

            await currentChannel.send("inviting {}".format(member.mention))


def setup(bot):
    bot.add_cog(Invite(bot))
