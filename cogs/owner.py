import os
import sys
import discord
import asyncio
from discord.ext import commands
from core.utils import send_embed

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


class owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown")
    async def shutdown(self, context):
        """
        Make the bot shutdown
        """
        if context.message.author.id in config.OWNERS:
            await send_embed("","Shutting down. Bye! :wave:")
            await self.bot.logout()
            await self.bot.close()
        else:
            async send_embed("Error!","You don't have the permission to use this command.")

    @commands.command(name="say", aliases=["echo"])
    async def say(self, context, *, args):
        """
        The bot will say anything you want.
        """
        if context.message.author.id in config.OWNERS:
            await context.send(args)
        else:
            send_embed("Error!","You don't have the permission to use this command.")

    @commands.command(name="embed")
    async def embed(self, context, *, args):
        """
        The bot will say anything you want, but within embeds.
        """
        if context.message.author.id in config.OWNERS:
            await send_embed("",args)
        else:
            await send_embed("Error!","You don't have the permission to use this command.")

def setup(bot):
    bot.add_cog(owner(bot))
