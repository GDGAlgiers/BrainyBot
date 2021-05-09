"""
    This cog will hold some general commands  like serverinfo,ping... 
"""

import os
import sys
import discord
from discord.ext import commands
from json import loads,dumps
from core.utils import send_embed, loads_to_object
from core.errors import *



if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    config = loads_to_object("config.json")



# This will define a cog named general
class general(commands.Cog, name="general"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo")
    async def serverinfo(self, context):
        """
        Get some useful (or not) information about the server.
        """
        server = context.message.guild
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = discord.Embed(
            title="**Server Name:**",
            description=f"{server}",
            color=int(config.EMBED_COLOR,16)
        )
        embed.set_thumbnail(
            url=server.icon_url
        )
        embed.add_field(
            name="Owner",
            value=f"{server.owner}\n{server.owner.id}"
        )
        embed.add_field(
            name="Server ID",
            value=server.id
        )
        embed.add_field(
            name="Member Count",
            value=server.member_count
        )
        embed.add_field(
            name="Text/Voice Channels",
            value=f"{channels}"
        )
        embed.add_field(
            name=f"Roles ({role_length})",
            value=roles
        )
        embed.set_footer(
            text=f"Created at: {time}"
        )
        await context.send(embed=embed)

    @commands.command(name="ping")
    async def ping(self, context):
        """
        Check if the bot is alive.
        """
        embed = discord.Embed(
            color=int(config.EMBED_COLOR,16)
        )
        embed.add_field(
            name="Pong!",
            value=":ping_pong:",
            inline=True
        )
        embed.set_footer(
            text=f"🏓 Pong Catch it if you can!{context.message.author}"
        )
        await context.send(embed=embed)

    @commands.command(name="server")
    async def server(self, context):
        """
        Get the invite link of the discord server of the bot for some support.
        """
        await context.send("I sent you a private message!")
        await context.author.send("Join my discord server by clicking here: https://www.gdgalgiers.com/discord")

    @commands.command(name="poll")
    async def poll(self, context, *args):
        """
        Create a poll where members can vote.
        """
        poll_title = " ".join(args)
        embed = discord.Embed(
            title="A new poll has been created!",
            description=f"{poll_title}",
            color=int(config.EMBED_COLOR,16)
        )
        embed.set_footer(
            text=f"Poll created by: {context.message.author} • React to vote!"
        )
        embed_message = await context.send(embed=embed)
        await embed_message.add_reaction("👍")
        await embed_message.add_reaction("👎")
        await embed_message.add_reaction("🤷")

    @commands.dm_only()
    @commands.command(name="isSpotOpen")
    async def isSpotOpen(self, context):
        """
        check if the GDG Algiers spot is open or not
        """
        if loads(open('config.json','r').read().strip())['spot']:
            sit="Open"
        else:
            sit="Close"
        await send_embed(context,"",f"Currently, the spot is {sit}.")

    @commands.dm_only()
    @commands.command(name="spot")
    async def spot(self, context):
        """
        open the spot if its closed or close it if opened
        """
        # if user is not a comanager he is not authorized
        # only comanagers has keys to open spot 
        if context.message.author.id not in config.COMANAGERS_IDs:
            raise AuthorizationError()
        else:
            dict=loads(open('config.json','r').read().strip())
            with open('config.json','w+') as f:
                if dict["spot"]:
                    dict["spot"]=False
                    new_value="Closed"
                    f.write(dumps(dict))
                else:
                    dict["spot"]=True
                    new_value="Open"
                    f.write(dumps(dict))
            await send_embed(context,"",f"Now, the spot became {new_value}.")


def setup(bot):
    bot.add_cog(general(bot))
