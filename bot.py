#!/usr/bin/python3 
"""
    #######################################################################################
                        This is the main file for our bot it contains initialization      #
                                And call for all the cogs                                 #
                                                                                          #
    #######################################################################################

"""
import discord
import asyncio
import os
import platform
import sys
import datetime
import time 
from discord.ext import commands,tasks
from core.utils import getchannel,getuser,getguild
from keep_alive import keep_alive
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config



intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True
intents.emojis = True

bot = commands.Bot(command_prefix=config.BOT_PREFIX, intents=intents)

# The code in this even is executed when the bot is ready


@bot.event
async def on_ready():
    bot.loop.create_task(status_task())
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print("-------------------")

# Setup the game status task of the bot


async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game("with you!"))
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Game("with Kero"))
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Game(f"{config.BOT_PREFIX} help"))
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Game("with humans!"))
        await asyncio.sleep(60)
# this is very important we will not use the default help command .


# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")

# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_command_completion(ctx):
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    guild_name = "Private DM "
    if ctx.guild:
        guild_name =ctx.guild.name
    print(
        f"Executed {executedCommand} command in {guild_name} by {ctx.message.author} (ID: {ctx.message.author.id})")



# The code in this event is executed every time a valid commands catches an error
@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(
            title="Error!",
            description="This command is on a %.2fs cooldown" % error.retry_after,
            color=0x00FF00
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.errors.PrivateMessageOnly):
        embed = discord.Embed(
            title="DMs only",
            description="This service is only available in direct messages",
            colour=discord.Colour.gold()
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        embed = discord.Embed(
            title="Missing Arguments",
            description="you need to specify the UUID",
            colour=discord.Colour.gold()
        )
        await context.send(embed=embed)
    raise error
        


# This will load the cogs set in startup cogs !!
# with this  we can specify the commands that we need and the one we don't !
if __name__ == "__main__":
    for extension in config.STARTUP_COGS:
        try:
            bot.load_extension(extension)
            extension = extension.replace("cogs.", "")
            print(f"Loaded extension '{extension}'")
        except Exception as e:
            exception = f"{type(e).__name__}: {e}"
            extension = extension.replace("cogs.", "")
            print(f"Failed to load extension {extension}\n{exception}")
    # run this function to launch the background job
    keep_alive()
    print(config.TOKEN)
    # Run the bot with the token
    bot.run(config.TOKEN)
