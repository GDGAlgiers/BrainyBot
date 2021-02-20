"""
    This is where we will put all our hashcode commands
"""
import time
import os
import sys
import discord
from discord.ext import commands
from discord.ext.commands import dm_only
from discord.utils import get
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
    if not os.path.isfile("gsp_creds.json"):
        sys.exit("'gsp_creds.json' not found! Please add it and try again.")
    else:
        gc = gspread.service_account(filename='gsp_creds.json',scopes=SCOPES)

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
        

    @commands.command(name="checkin")
    async def checkin(self, ctx):
        "Command Description"
        if ctx.author.id in users:
            await ctx.author.send(Error("Already logged in!"))
        else:
            user_id = ctx.author.id
            users[user_id]={
                "lastactive" : time.time()
            }
            embed = discord.Embed(
                title="Join", description="List of available commands:", color=0x00FF00)
            embed.add_field(name='Join',value = "$join \" PASSWORD \"\nMake sure you execute it at DM",inline=False)
            await ctx.author.send(embed=embed)


    @dm_only()
    @commands.command(name="join")
    async def join(self, ctx,uuid: str):
        if ctx.author.id not in users:
            await ctx.author.send(embed=Error("Not logged in!"))
        else:
            if len(uuid) != UUID_LENGTH :
                await ctx.send(embed=Error("Wrong UUID !"))
            else:
                await ctx.send("Please be patient!")
                #Authentication
                TeamExist,TeamName=Auth(uuid)
                if not TeamExist:
                    await ctx.send(embed=Error("Wrong UUID !"))
                else:
                    #retrieving the Server guild
                    guild = self.bot.guilds[0]
                    
                    #sending logs to logs channel 
                    log_channel = get(guild.text_channels, name="logs")
                    await log_channel.send(f"{ctx.author} has joined {TeamName}_team .")
                    
                    member=ctx.author
                    overwrites = discord.PermissionOverwrite(
                                view_channel=True,
                                read_messages=True,
                                read_message_history=True,
                                send_messages=True,
                                embed_links=True,
                                attach_files=True,
                                add_reactions=True,
                                connect=True,
                                speak=True,
                                stream=True
                            )
                        
                    #verifying if the category is already created
                    categories = guild.categories
                    team_category=list(filter(lambda category:category if category.name == f"{TeamName}_category" else None,categories))
                    if team_category :
                        team_category = team_category[0]


                        await team_category.set_permissions(member, overwrite=overwrites)
                        await ctx.send(f"You have been successfully added to {TeamName}_channels! ")
                    else: #Creating the category and its channels
                        try:
                            '''
                            category_overwrites = discord.PermissionOverwrite(
                                view_channel=False,
                                read_messages=False,
                                read_message_history=False,
                                send_messages=False,
                                embed_links=False,
                                attach_files=False,
                                add_reactions=False,
                                connect=False,
                                speak=False,
                                stream=False
                            )
                            '''
                            category = await guild.create_category(f"{TeamName}_category", overwrites=None, reason=None)
                            
                            await category.set_permissions(member, overwrite=overwrites)
                            await guild.create_voice_channel(f"voice-channel", overwrites=None, category=category, reason=None)
                            await guild.create_text_channel(f"text-channel", overwrites=None, category=category, reason=None)
                            await ctx.send(f"{TeamName}_channels are Created Successfully!")
                        except Exception as errors:
                            print(f"Bot Error: {errors}")
        


def setup(bot):
    @loop(minutes=INACTIVE_TIMEOUT)
    async def logout_inactive():
        for user_id in list(users):
            if time.time() - users[user_id]["lastactive"] > INACTIVE_TIMEOUT:
                users.pop(user_id)
                await bot.get_user(user_id).send(":timer: Logged out due to inactivity")
    logout_inactive.start()
    bot.add_cog(hashcode(bot))
