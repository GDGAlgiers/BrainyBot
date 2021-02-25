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
from core.db import db
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



@bot.event
async def on_raw_reaction_add(payload):
    reaction = str(payload.emoji)
    msg_id = payload.message_id
    ch_id = payload.channel_id
    user_id = payload.user_id
    guild_id = payload.guild_id
    exists = db.exists(msg_id)

    if isinstance(exists, Exception):
        await print(
            f"Database error after a user added a reaction:\n```\n{exists}\n```",
        )

    elif exists:
        # Checks that the message that was reacted to is a reaction-role message managed by the bot
        reactions = db.get_reactions(msg_id)

        if isinstance(reactions, Exception):
            await print(

                f"Database error when getting reactions:\n```\n{reactions}\n```",
            )
            return

        ch = await getchannel(bot,ch_id)
        msg = await ch.fetch_message(msg_id)
        user = await getuser(bot,user_id)
        if reaction not in reactions:
            # Removes reactions added to the reaction-role message that are not connected to any role
            await msg.remove_reaction(reaction, user)

        else:
            # Gives role if it has permissions, else 403 error is raised
            role_id = reactions[reaction]
            server = await getguild(bot,guild_id)
            member = server.get_member(user_id)
            role = discord.utils.get(server.roles, id=role_id)
            if user_id != bot.user.id:
                try:
                    await member.add_roles(role)

                except discord.Forbidden:
                    await print(

                        "Someone tried to add a role to themselves but I do not have"
                        " permissions to add it. Ensure that I have a role that is"
                        " hierarchically higher than the role I have to assign, and"
                        " that I have the `Manage Roles` permission.",
                    )


@bot.event
async def on_raw_reaction_remove(payload):
    reaction = str(payload.emoji)
    msg_id = payload.message_id
    user_id = payload.user_id
    guild_id = payload.guild_id
    exists = db.exists(msg_id)

    if isinstance(exists, Exception):
        await print(

            f"Database error after a user removed a reaction:\n```\n{exists}\n```",
        )

    elif exists:
        # Checks that the message that was unreacted to is a reaction-role message managed by the bot
        reactions = db.get_reactions(msg_id)

        if isinstance(reactions, Exception):
            await print(
                f"Database error when getting reactions:\n```\n{reactions}\n```",
            )

        elif reaction in reactions:
            role_id = reactions[reaction]
            # Removes role if it has permissions, else 403 error is raised
            server = await getguild(bot,guild_id)
            member = server.get_member(user_id)

            if not member:
                member = await server.fetch_member(user_id)

            role = discord.utils.get(server.roles, id=role_id)
            try:
                await member.remove_roles(role)

            except discord.Forbidden:
                await print(
                    "Someone tried to remove a role from themselves but I do not have"
                    " permissions to remove it. Ensure that I have a role that is"
                    " hierarchically higher than the role I have to remove, and that I"
                    " have the `Manage Roles` permission.",
                )






# The code in this event is executed every time a command has been *successfully* executed
@bot.event
async def on_command_completion(ctx):
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    print(
        f"Executed {executedCommand} command in {ctx.guild.name} by {ctx.message.author} (ID: {ctx.message.author.id})")



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
        


######################### HashCOde Timer ###############################################


message_sent = False 

@tasks.loop(seconds=1.0)
async def timer():
    curr = datetime.datetime.now
    await bot.wait_until_ready()
    channel = bot.get_channel(config.HASHCODE_GENERAL_CHANNEL_ID)
    global message_sent
    if config.HASHCODE_START_DATE.hour == curr().hour and config.HASHCODE_START_DATE.minute ==curr().minute and curr().second == 57:
      if not message_sent:
        await channel.send('3')
        time.sleep(1)
        await channel.send('2')
        time.sleep(1)
        await channel.send('1')
        time.sleep(1)
        await channel.send('***GOO***')
        message_sent = True
    

    
    lasth =config.HASHCODE_END_DATE.hour-curr().hour
    lastm =config.HASHCODE_END_DATE.minute-curr().minute
    lasts =config.HASHCODE_END_DATE.second-curr().second
    if lasth == 1:
      if lastm == 0 and lasts == 0:
       await channel.send("Only one hour separates us from the official start of the most awaited HashCode competition :partying_face: We can hear your hearts beating fast :eyes:")
      elif lastm == -30 and lasts == 0:
        await channel.send("Tik Tok :stopwatch: We hope you didn't fall asleep because only 30 minutes are left for the competition :heart_eyes:  HOW EXCITING IS THAT!! :star_struck:")
    elif lastm==30 and lasts==0 and lasth == 0:
      await channel.send("Tik Tok :stopwatch: We hope you didn't fall asleep because only 30 minutes are left for the competition :heart_eyes:  HOW EXCITING IS THAT!! :star_struck:")
    elif lastm==1 and lasth == 0:
      lasts =(60+ config.HASHCODE_END_DATE.second)-curr().second
      if lasts == 10:
        for i in range(10,0,-1):
          await channel.send(str(i)+" seconds :hourglass:")
          time.sleep(1)
        await channel.send("**TIME OVER** :alarm_clock:")
    elif lasth == 0 and lastm == 0:
      if lasts == 10:
        for i in range(10,0,-1):
          await channel.send(str(i)+" seconds :hourglass:")
          time.sleep(1)
        await channel.send("**TIME OVER** :alarm_clock:")


dt = datetime.datetime.now()

if (dt.year==config.HASHCODE_START_DATE.year and dt.month==config.HASHCODE_START_DATE.month and dt.day==config.HASHCODE_START_DATE.day and dt.hour <= config.HASHCODE_END_DATE.hour ):
    timer.start()


######################### HashCOde Timer ###############################################

# run this function to launch the background job
keep_alive()


# Run the bot with the token
bot.run(config.TOKEN)
