# Base code:
import discord
from discord.ext import commands,tasks
from discord.utils import get
import time 
import datetime
from datetime import timedelta

# Granting permission to see the members and their messages.
intents = discord.Intents(messages=True, members=True, guilds=True)

# Setting up the bot and the prefix for its use and set the bot's permissions.
bot = commands.Bot(command_prefix="$", intents=intents)


# This executes when the bot is online in Discord
@bot.event 
async def on_ready():
  print("bot is ready")

curr = datetime.datetime.now

start = {
  "hours": 23,
  "minutes": 53,
  "seconds": 20
}

end = {
  "hours" : 23,
  "minutes" : 49,
  "seconds": 0
}

message_sent = False 

@tasks.loop(seconds=1.0)
async def timer():
  await bot.wait_until_ready()
  channel = bot.get_channel(811398968030003250)
  global message_sent
  if start["hours"] == curr().hour and start["minutes"] ==curr().minute and curr().second == 57:
    if not message_sent:
      await channel.send('3')
      time.sleep(1)
      await channel.send('2')
      time.sleep(1)
      await channel.send('1')
      time.sleep(1)
      await channel.send('***GOO***')
      message_sent = True
  

  
  lasth =end["hours"]-curr().hour
  lastm =end["minutes"]-curr().minute
  lasts =end["seconds"]-curr().second
  if lasth == 1:
    if lastm == 0 and lasts == 0:
     await channel.send("1 hour left :hourglass_flowing_sand:")
    elif lastm == -30 and lasts == 0:
      await channel.send("30 minutes left :hourglass:")
  elif lastm==30 and lasts==0 and lasth == 0:
    await channel.send("30 minutes left :hourglass:")
  elif lastm==1 and lasth == 0:
    lasts =(60+ end["seconds"])-curr().second
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

  print(lasth)
  print(lastm)
  print(lasts)
 
timer.start()

# Run the bot using the tokenID 
bot.run("ODAxOTI2NTM2ODQ0Mjc5ODI3.YAnySQ.0cqDN_4aEYlkjuPOrwSM1SevuJM")
