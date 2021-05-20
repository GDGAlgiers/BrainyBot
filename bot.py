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
from aiohttp import ClientSession
from discord.ext import commands,tasks
from core.utils import getchannel,getuser,getguild
from keep_alive import keep_alive
from core.utils import send_embed,loads_to_object
from core import errors
from json import  loads


if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    config = loads_to_object("config.json")



intents = discord.Intents.default()
intents.members = True
intents.reactions = True
intents.messages = True
intents.emojis = True

bot = commands.Bot(command_prefix=config.BOT_PREFIX, intents=intents)
bot.session = ClientSession()

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
        await bot.change_presence(activity=discord.Game(f"{config.BOT_PREFIX} help"))
        await asyncio.sleep(60)
        await bot.change_presence(activity=discord.Game("with humans!"))
        await asyncio.sleep(60)


# this is very important we will not use the default help command .
# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")


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
    # here we log the error
    print("Error type:", type(error))

    # then handle it !
    if isinstance(error, commands.CommandOnCooldown):
        await send_embed(context,"Error!","This command is on a %.2fs cooldown" % error.retry_after)
    elif isinstance(error, commands.errors.PrivateMessageOnly):
        await send_embed(context,"DMs only","This service is only available in direct messages",discord.Colour.gold())
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await send_embed(context,"Missing Arguments","you need to specify the UUID",discord.Colour.gold())
    elif isinstance(error, discord.Forbidden):
        await send_embed(context,"Permission Denied","I don't have permissions to post in that channel",discord.Colour.gold())
    elif isinstance(error,errors.AuthorizationError):
        await send_embed(context,"Error!","You don't have the permission to use this command.")
    elif isinstance(error,errors.HackTheBotUnknownError):
        await send_embed(context,"Error!",":frowning2:  Sorry i got an unkown error , can you please report this to the admins :pray: ")
    elif isinstance(error,errors.HackTheBotNotRegistered):
        await send_embed(context,"Not Registered !","It seems that you still has **not registered** to Our Event :eyes:   **OR** you have already registered :white_check_mark:  but you **didn't confirm** :ok: \n if this is the case please confirm by clicking the **confirm button** in the confirmation email :ok:")
    elif isinstance(error,errors.HackTheBotInvalidTeamName):
        await send_embed(context,"Invalid Team Name","Sorry you have submitted a wrong team name ! ")
    elif isinstance(error,commands.errors.CommandNotFound):
        await send_embed(context,"Invalid Command","Sorry I don't understand this command")

#    elif isinstance(error,asyncio.exceptions.TimeoutError):
#        await send_embed(context,"Timeout ","Message announcement creation failed, you took too long to provide the requested information.")
    else:
        print("Uncaught error !")
        print("Error type:", type(error))
        print("Error message:", error)
        await context.send(":x: Error")
        raise error
        
        

#  get the discord token 
if "DISCORD_TOKEN" in os.environ :
    TOKEN = os.getenv("DISCORD_TOKEN")
else:
    configJson = loads(open("config.json","r").read())
    TOKEN = configJson["DISCORD_TOKEN"]
    
if TOKEN == None:
    raise "Server token not found"

# run this function to launch the background job
# this function is very util when you run your bot on environment 
# that kills your process
keep_alive()

# Run the bot with the token
bot.run(TOKEN)
