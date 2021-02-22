"""
    This is where we will put all our hashcode commands
"""
import time
import os
import asyncio
import re
import datetime
import sys
import discord
from discord.ext import commands
from discord.ext.commands import dm_only
from discord.utils import get
from core.utils import message_check
from hashlib import md5
from discord.ext.tasks import loop
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


UUID_LENGTH=19
# timeout for logging out an inactive user
INACTIVE_TIMEOUT = 1
#stores the users logged in and their last time active 
users = dict()



def Error(message):
    embed = discord.Embed(
            title="Joining failure",
            description=str(message),
            colour=discord.Colour.red()
        )
    return embed

def Auth(uuid):
    hashed_uuid = md5(uuid.encode()).hexdigest()
    SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
    ]
    import gspread
    if not os.path.isfile("brainy.json"):
        sys.exit("'brainy.json' not found! Please add it and try again.")
    else:
        gc = gspread.service_account(filename='brainy.json',scopes=SCOPES)

    sheet_name = "hashcode-gdg-hub-contestants"
    sheet = gc.open(sheet_name).get_worksheet(0).get_all_records()
    TeamName=None
    exist=False
    for i in range(len(sheet)):
        if sheet[i]['hashed_uuid'] == hashed_uuid:
            exist=True
            TeamName=sheet[i]['teamName']
            break
    return exist,TeamName
   
    

class hashcode(commands.Cog, name="hashcode"):
    def __init__(self, bot):
        self.bot = bot
        # get the time left to end of the hashcode
        self.start_time = datetime.datetime(2021, 2, 25, 18, 30, 0, 0)
        self.duration = datetime.timedelta(hours=4)
        self.end = self.start_time + self.duration

    @commands.command(description="Get the time left to the end of the competition")
    async def timeLeft(self, ctx):
        now = datetime.datetime.now()
        if now > self.end:
            await ctx.message.channel.send(f"The contest has ended :) ")
        elif now< self.start_time:
            await ctx.message.channel.send(f"The contest has still not started :) ")
        else:
            delta = self.end - now
            hours_left = delta.seconds // 3600
            minutes_left = (delta.seconds % 3600) // 60
            seconds_left = (delta.seconds % 3600 ) % 60
            await ctx.message.channel.send(f"Time left {hours_left}hours {minutes_left}minutes {seconds_left}seconds")

    @commands.command(name="checkin")
    async def checkin(self, ctx):
        """ Start check-in to join your private workspace"""
        """
        if ctx.channel.id is not 775491463940669480:
            return
        """
        if ctx.author.id in users:
            await ctx.author.send(embed=Error("Already logged in!"))
        else:
            participant = {}
            user_id = ctx.author.id
            try:
                sent_initial_message = await ctx.author.send("Hello To checkin fonctionality please provide us your key ")
                response = await self.bot.wait_for('message',timeout=120, check=message_check(channel=ctx.author.dm_channel))
            except asyncio.TimeoutError: 
                await ctx.author.send("you took too long to provide the requested information.")
            finally:
                await sent_initial_message.delete()
            uuid  = response.content.strip()
            if len(uuid) != UUID_LENGTH or  not re.match(r'[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}',uuid) :
                await ctx.author.send(embed=Error("Wrong UUID !"))
            else:
                users[user_id]={
                "lastactive" : time.time()
                }
                TeamExist,TeamName=Auth(uuid)
                #retrieving the Server guild
                guild = self.bot.guilds[0]                  
                workspace_category = guild.get_channel(config.HASHCODE_CATEGORY_WORKSPACE_ID)
                print(guild)
                print(guild.roles)
                team_role = get(guild.roles, name=f"{TeamName}_member")
                if team_role:
                    if team_role in ctx.author.roles:
                        await ctx.author.send(embed=Error("You have already joined your space"))
                    else:
                        print(team_role)
                        await ctx.author.add_roles(team_role)
                        await ctx.author.send(":white_check_mark: WELCOME TO GDG ALGIERS HUB")
                        #sending logs to logs channel 
                        log_channel = guild.get_channel(config.HASHCODE_LOGS_CHANNEL_ID)
                        await log_channel.send(f" @{ctx.author} has joined {TeamName}_team .")
                else:
                    await guild.create_role(name=f"{TeamName}_member")
                    role = get(guild.roles, name=f"{TeamName}_member")
                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        guild.me: discord.PermissionOverwrite(read_messages=True),
                        role: discord.PermissionOverwrite(read_messages=True)
                    }
                    try:
                        channel = await guild.create_text_channel(f"{TeamName}_space",category=workspace_category, overwrites=overwrites)
                        channel_voice = await guild.create_voice_channel(f"{TeamName}_space",category=workspace_category, overwrites=overwrites)
                    except Exception as errors:
                        print(f"Bot Error: {errors}")
                    finally:
                        await ctx.author.add_roles(role)
                        await ctx.author.send(":white_check_mark: WELCOME TO GDG ALGIERS HUB")
                        #sending logs to logs channel 
                        log_channel = guild.get_channel(config.HASHCODE_LOGS_CHANNEL_ID)
                        await log_channel.send(f" @{ctx.author} has joined {TeamName}_team .")
                

        


def setup(bot):
    bot.add_cog(hashcode(bot))
