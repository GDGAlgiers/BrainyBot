import discord
import os
from discord.ext import commands
from discord.utils import get


# Granting permission to see the members and their messages.
intents = discord.Intents(messages=True, members=True, guilds=True)

# Setting up the bot and the prefix for its use and set the bot's permissions.
bot = commands.Bot(command_prefix="!", intents=intents)


# This executes when the bot is online in Discord
@bot.event 
async def on_ready():
  print("bot is ready")

# Setting up the first command '!hello'
@bot.command()
async def hello(ctx):
  await ctx.message.channel.send("Hello :pray:")

@bot.command()
async def post(ctx,*args):
  if (len(args)<2 or args[0][0:1]!="@"):
    await ctx.message.channel.send("invalid parametres\nsynthaxe : !post @channel_id message")
  else : 
    channel = discord.utils.get(ctx.guild.channels, name=args[0][1:])
    if (channel==None) :
      await ctx.message.channel.send('channel "{}" introuvable'.format(args[0][1:]))
    else:
      await channel.send(' '.join(args[1:]))
    
 


# Run the bot using the tokenID 
bot.run("ODAxOTI2NTM2ODQ0Mjc5ODI3.YAnySQ.0cqDN_4aEYlkjuPOrwSM1SevuJM")