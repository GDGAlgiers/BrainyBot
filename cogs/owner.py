import os
import sys
import discord
import asyncio
from discord.ext import commands
from core.utils import send_embed,loads_to_object
from core.errors import AuthorizationError

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    config = loads_to_object("config.json")


class owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown")
    async def shutdown(self, context):
        """
        Make the bot shutdown
        """
        if context.message.author.id in config.OWNERS:
            await send_embed(context,"","Shutting down. Bye! :wave:")
            await self.bot.logout()
            await self.bot.close()
        else:
            raise AuthorizationError()

    @commands.command(name="say", aliases=["echo"])
    async def say(self, context, *, args):
        """
        The bot will say anything you want.
        """
        if context.message.author.id in config.OWNERS:
            await context.send(args)
        else:
            raise AuthorizationError()

    @commands.command(name="embed")
    async def embed(self, context, *, args):
        """
        The bot will say anything you want, but within embeds.
        """
        if context.message.author.id in config.OWNERS:
            await send_embed(context,"",args)
        else:
            raise AuthorizationError()

def setup(bot):
    bot.add_cog(owner(bot))
