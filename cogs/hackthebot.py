import os
import sys
import discord
from discord.ext import commands
from json import loads,dumps
from core.utils import send_embed, loads_to_object,getchannel,getguild
from core.errors import *

from discord.utils import get

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    config = loads_to_object("config.json")


class hackthebot(commands.Cog, name="hackthebot"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.dm_only()
    @commands.command(name="verify")
    async def verify(self, context):
        """
            Verify if the user is a participant of hack the bot !
        """
        user_id = context.author.id
        await context.trigger_typing()
        async with self.bot.session.post(config.HACK_THE_BOT_URL+"/api/verify", json={"participant_id":user_id}) as r:
            res = await r.json()
            if res["status"] =='UNAUTHORIZED':
                raise HackTheBotNotRegistered()
            elif res["status"] =='UNKNOWN_ERROR':
                raise HackTheBotUnknownError()
            elif res["status"] =='SUCCESS':
                embed = discord.Embed(
                    title="PARTICIPANT",
                    description="How can i help you **participant** :thinking: , You have registered **successfully** :white_check_mark:  Can't wait to say what you will made during the Hackathon :star_struck:",
                    color=int(config.EMBED_COLOR,16)
                )
                await context.author.send(embed=embed)
            else:
                raise HackTheBotUnknownError()

         
    @commands.command(name="help-mentor")
    async def help_mentor(self,context : commands.Context):
        """
            Calls a mentor to help the team
        """
        await context.trigger_typing()
        guild = context.guild
        text_channel = context.channel
        #TODO* Getting the voice_channel with the same name as text channel
        voice_channel = discord.utils.find(lambda c: c.name == context.channel.name, guild.voice_channels)
        parts = text_channel.name.split("-")
        if len(parts) == 2 and parts[1] == "hackthebot":
            role_name = "HTB-mentor"
            role = get(guild.roles, name=role_name)
            permission = text_channel.overwrites.get(role,None)
            if(permission is not None and permission.read_messages is True and permission.send_messages is True):
                embed = discord.Embed(
                    title="CHECK YOUR CHANNEL",
                    description="A mentor should be there with you, if not please wait for them",
                    color=int(config.EMBED_COLOR,16)
                )
                await context.channel.send(embed=embed)
                return
            else:
                print(f"Adding ${role} role to text channel ${text_channel}")
                await text_channel.set_permissions(role, read_messages=True,
                                                      send_messages=True)
            
                print(f"Adding ${role} role to voice channel ${voice_channel}")
            
                if voice_channel is not None:
                    await voice_channel.set_permissions(role, read_messages=True,
            
                                                      send_messages=True)
                embed = discord.Embed(
                    title="HELP MENTOR",
                    description="A mentor will be coming your way...stay tight",
                    color=int(config.EMBED_COLOR,16)
                )
                await context.channel.send(embed=embed)                                          
                # Sending log message to mentors to alert them
                mentor_logs_channel = get(guild.channels, name="mentors-log")
                team = parts[0]
                embed = discord.Embed(
                    title="Team needs help",
                    description=f"Team {team} is looking for a mentor, please help them",
                    color=int(config.EMBED_COLOR,16)
                )
                await mentor_logs_channel.send(embed=embed)
        else:
            raise HackTheBotUnknownError(message="Command can only be issued from a team channel")

                  
    @commands.command(name="thanks-mentor")
    async def thanks_mentor(self,context):
        """
            Says thank you to mentor and asks him to leave :)
        """
        await context.trigger_typing()
        guild = context.guild
        # for testing only 
        text_channel = context.channel
        print(guild.voice_channels)
        #TODO* Getting the voice_channel with the same name as text channel
        voice_channel = discord.utils.find(lambda c: c.name == context.channel.name, guild.voice_channels)
        parts = text_channel.name.split("-")
        if len(parts) == 2 and parts[1] == "hackthebot":
            role_name = "HTB-mentor"
            role = get(guild.roles, name=role_name)
            permission = text_channel.overwrites.get(role,None)
            if(permission is None or  permission.read_messages is False and permission.send_messages is False):
                embed = discord.Embed(
                    title="NO MENTORS HERE",
                    description="No mentor is allowed to see your channel don't worry",
                    color=int(config.EMBED_COLOR,16)
                )
                await context.channel.send(embed=embed)
                return
            else:
                print(f"Removing ${role} role to text channel ${text_channel}")
                await text_channel.set_permissions(role, read_messages=False,
                                                      send_messages=False)
            
                print(f"Removing ${role} role to voice channel ${voice_channel}")
            
                if voice_channel is not None:
                    await voice_channel.set_permissions(role, read_messages=False,
                                                      send_messages=False) 
                embed = discord.Embed(
                    title="THANKS MENTOR",
                    description="Got your help ? get back to hacking",
                    color=int(config.EMBED_COLOR,16)
                )
                await context.channel.send(embed=embed)                                         
        else:
            raise HackTheBotUnknownError(message="Command can only be issued from a team channel")


# utils functions    
def fetch_issuer_channel(context):
    """
    Gets issuer of command channel from api 
    """
    channel = "team1-hackthebot"
    return channel 


def setup(bot):
    bot.add_cog(hackthebot(bot))