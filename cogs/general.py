"""
    This cog will hold some general commands  like serverinfo,ping... 
"""

import os
import sys
import discord
from discord.ext import commands
from json import loads,dumps
from core.utils import send_embed
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config



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
            color=0x00FF00
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
            color=0x00FF00
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
        await context.author.send("Join my discord server by clicking here: https://discord.gg/zeTe8Um2Ca")

    @commands.command(name="poll")
    async def poll(self, context, *args):
        """
        Create a poll where members can vote.
        """
        poll_title = " ".join(args)
        embed = discord.Embed(
            title="A new poll has been created!",
            description=f"{poll_title}",
            color=0x00FF00
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
        know if the spot is open or not
        """
        if loads(open('spot.json','r').read().strip())['spot']:
            sit="Open"
        else:
            sit="Close"

        await send_embed("",f"Currently, the spot is {sit}.")

    @commands.dm_only()
    @commands.command(name="spot")
    async def spot(self, context):
        """
        open the spot and close it
        """
        if context.message.author.id not in config.COMANAGERS_IDs:
            await send_embed("","You are not allowed !")
        else:
            dict=loads(open('spot.json','r').read().strip())
            with open('spot.json','w+') as f:
                if dict["spot"]:
                    dict["spot"]=False
                    sit="Closed"
                    f.write(dumps(dict))
                else:
                    dict["spot"]=True
                    sit="Open"
                    f.write(dumps(dict))
            await send_embed("",f"Now, the spot became {sit}.")


def setup(bot):
    bot.add_cog(general(bot))
