"""
    This is where we will put all our hashcode commands
"""
import os
import sys
import discord
from discord.ext import commands
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


class hashcode(commands.Cog, name="hashcode"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test")
    async def test(self, context):
        "This is a test command"
        await context.send("This is a test command")
