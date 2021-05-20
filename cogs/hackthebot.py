import os
import sys
import discord
from discord.ext import commands
from json import loads,dumps
from core.utils import send_embed, loads_to_object,verify_api,getchannel,getguild
from core.errors import *
from discord.utils import get,find
import re,requests
import time
import asyncio
from pathlib import Path
import random
from hashlib import md5

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
        verify_api(user_id)
        embed = discord.Embed(
            title="PARTICIPANT",
            description="How can i help you **participant** :thinking: , You have registered **successfully** :white_check_mark:  Can't wait to say what you will made during the Hackathon :star_struck:",
            color=int(config.EMBED_COLOR,16)
        )
        await context.author.send(embed=embed)
    

    @commands.dm_only()
    @commands.command(name="createTeam")
    async def createTeam(self, context):
        """
            Create new Hack the bot team / Only team leader should create Team
        """
        user_id = context.author.id
        await context.trigger_typing()
        participant_id = verify_api(user_id)

        await context.send("This command will allow you to create a new team :people_with_bunny_ears_partying:  , "\
            "Please provide the required information once requested :blush:. If you would like to abort the creation, "\
            "do not respond and I will move on.")
        time.sleep(1)
        await context.trigger_typing()
        data = {}

        ## get team name 
        await context.send("Please give me the your team name :blush: ! Team name must be alphanumeric  only  and length less than 25")
        try:
            team_name_message = await self.bot.wait_for('message', timeout=120, check=lambda message: message.author.id == context.message.author.id and message.content != "" )
            team_name = team_name_message.content.lower()

            if len(team_name)> 25 or not team_name.isalnum():
                raise HackTheBotInvalidTeamName()
            data["name"] = team_name
        except asyncio.TimeoutError: 
            await send_embed(context, "Cancelled" ,":octagonal_sign: Command cancelled")
            await context.author.send("you took too long to provide the requested information.")
            return 

        ## get team image 
        time.sleep(1)
        await context.trigger_typing()
        await context.send("The next step is to pass me an image :sunrise_over_mountains: that represents your team. This step is totally optional, send NONE if you don't want to set image  ")
        validfiles = [".jpg", ".jpeg", ".gif", ".png", ".bmp"]
        data["image"] = "https://firebasestorage.googleapis.com/v0/b/gdg-wtm-website.appspot.com/o/BrainyPdp.png?alt=media&token=69c27608-fbe9-4785-b845-5bc5f0de4830"
        try:
            team_image_message = await self.bot.wait_for('message', timeout=120, check=lambda message: message.author.id == context.message.author.id  )
            if team_image_message.content !="NONE":
                if(len(team_image_message.attachments))>0:
                    attachment = Path(team_image_message.attachments[0].filename)
                    # verify its an image 
                    if attachment.suffix in validfiles:
                        imageurl = team_image_message.attachments[0].url
                        data["image"]= imageurl
                    else:
                        await send_embed(context, "Cancelled" ,"An invalid file attached :octagonal_sign:, we accept the following formats only :  .jpg , .jpeg , .gif , .png , .bmp")
                        return
                else:
                    await send_embed(context, "Cancelled" ,"No Attachments have been sent !")
                    return
        except asyncio.TimeoutError: 
            await send_embed(context, "Cancelled" ,":octagonal_sign: Command cancelled")
            await context.author.send("you took too long to provide the requested information.")
            return 
        token = md5(os.urandom(8)+data["name"].encode()).hexdigest()
        data["token"] = token
        r =  requests.post(config.HACK_THE_BOT_URL+f"/api/participant/{participant_id}/team/create", json=data) 
        response = r.json()
        if(response["status"] =="ALREADY_IN_A_TEAM"):
            embed = discord.Embed(
                    title="Already have a team",
                    description="You already have a team...Good luck with your hack :muscle:",
                    color=int(config.EMBED_COLOR,16)
            )
            await context.author.send(embed=embed)
            return
        elif response["status"] =='TEAM_ALREADY_EXIST':
            embed = discord.Embed(
                    title="Team Already exist",
                    description="Team Already exists with this name... be more creative :stuck_out_tongue:",
                    color=int(config.EMBED_COLOR,16)
            )
            await context.author.send(embed=embed)
            return
        else:
            token = response["token"]
            embed = discord.Embed(
                    title="Team Created",
                    description=f"Team was created successfully :star_struck:...now your partners can join you using this key {token} by sending me a dm with the `$joinTeam` command ",
                    color=int(config.EMBED_COLOR,16)
            )
            await context.author.send(embed=embed)
        # TODO logg
        guild = self.bot.guilds[0]  
        first_category = guild.get_channel(config.HACK_THE_BOT_SPACES[0])
        text_channels_number = len(list(filter(lambda channel:str(channel.type) == 'text',first_category.channels)))
        space_category = first_category
        if text_channels_number > 24:
            space_category = guild.get_channel(config.HACK_THE_BOT_SPACES[1])
        
        team_role = get(guild.roles, name=f"{team_name}_hackthebot")
        # get the member to add him a role 
        user_id = context.author.id
        member = find(lambda m:m.id == user_id,guild.members)
        if team_role:
            await member.add_roles(team_role)
            await context.author.send("SUCCESS!! :white_check_mark:  Welcome abroad  :sunglasses: Good luck on the hack! :muscle:")
            #sending logs to logs channel 
            log_channel = guild.get_channel(config.HACK_THE_BOT_LOGS)
            embed = discord.Embed(
                title="Team Created",
                description=f"Team was created !!",
                color=int(config.EMBED_COLOR,16),
            )
            embed.set_thumbnail(url=data["image"])
            await log_channel.send(embed=embed)
        else:
            await guild.create_role(name=f"{team_name}_hackthebot")
            time.sleep(1)
            role = get(guild.roles, name=f"{team_name}_hackthebot")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                role: discord.PermissionOverwrite(read_messages=True)
            }
            try:
                channel = await guild.create_text_channel(f"{team_name}_space",category=space_category, overwrites=overwrites)
                channel_voice = await guild.create_voice_channel(f"{team_name}_space",category=space_category, overwrites=overwrites)
            except Exception as errors:
                print(f"Bot Error: {errors}")
            finally:
                await member.add_roles(role)
                await context.author.send("SUCCESS!! :white_check_mark:  Welcome abroad :sunglasses: Good luck on the hack! :muscle:")
                log_channel = guild.get_channel(config.HACK_THE_BOT_LOGS)
                embed = discord.Embed(
                    title="Team Created",
                    description=f"Team was created !!",
                    color=int(config.EMBED_COLOR,16),
                )
                embed.set_thumbnail(url=data["image"])
                await log_channel.send(embed=embed)

         
    @commands.command(name="helpMentor")
    async def help_mentor(self,context : commands.Context):
        """
            Calls a mentor to help the team
        """
        user_id = context.author.id
        verify_api(user_id)
        await context.trigger_typing()
        guild = context.guild
        text_channel = context.channel
        #TODO* Getting the voice_channel with the same name as text channel
        voice_channel = discord.utils.find(lambda c: c.name == context.channel.name, guild.voice_channels)
        parts = text_channel.name.split("_")
        if len(parts) == 2 and parts[1] == "hackthebot":
            role_name = "HTB-mentor"
            role = get(guild.roles, name=role_name)
            permission = text_channel.overwrites.get(role,None)
            if(permission is not None and permission.read_messages is True and permission.send_messages is True):
                embed = discord.Embed(
                    title="Check your channel",
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
                    title="Help Mentor",
                    description="A mentor will be coming your way...stay tight :star_struck:",
                    color=int(config.EMBED_COLOR,16)
                )
                await context.channel.send(embed=embed)                                          
                # Sending log message to mentors to alert them
                mentor_logs_channel = guild.get_channel(config.HACK_THE_BOT_LOGS)
                embed = discord.Embed(
                    title="Team needs help",
                    description=f"Team {text_channel.mention} is looking for a mentor, please help them :smiling_face_with_3_hearts:",
                    color=int(config.EMBED_COLOR,16)
                )
                await mentor_logs_channel.send(embed=embed)
        else:
            raise HackTheBotUnknownError(message="Command can only be issued from a team channel")

                  
    @commands.command(name="thanksMentor")
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
        parts = text_channel.name.split("_")
        if len(parts) == 2 and parts[1] == "hackthebot":
            role_name = "HTB-mentor"
            role = get(guild.roles, name=role_name)
            permission = text_channel.overwrites.get(role,None)
            if(permission is None or  permission.read_messages is False and permission.send_messages is False):
                embed = discord.Embed(
                    title="No mentors here",
                    description="No mentor is allowed to see your channel don't worry :wink: ",
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
                    title="Thanks mentor",
                    description="Got your help :white_check_mark: ? get back to hacking :muscle:",
                    color=int(config.EMBED_COLOR,16)
                )
                await context.channel.send(embed=embed)                                         
        else:
            raise HackTheBotUnknownError(message="Command can only be issued from a team channel")


    @commands.dm_only()
    @commands.command(name="joinTeam")
    async def joinTeam(self, context,token:str):
        """
            Join a team using a token given to the team leader (the one who created the team)/
            team must contain at most 3 members
        """
        user_id = context.author.id
        await context.trigger_typing()
        participant_id =  verify_api(user_id)
        # verify it is a participant and has no team 
        

        r =  requests.post(config.HACK_THE_BOT_URL+f"/api/participant/{participant_id}/team/join",
                         json={"token":token}) 
        res = r.json()
        if res["status"] =='UNKNOWN_ERROR':
            raise HackTheBotUnknownError()
        elif res["status"] == 'SUCCESS':
            team_name = res["team_name"]
            guild = self.bot.guilds[0] 
            team_role = get(guild.roles, name=f"{team_name}_hackthebot")
            member = find(lambda m:m.id == user_id,guild.members)
            await member.add_roles(team_role)
            await context.send(res['message'])
            log_channel = guild.get_channel(config.HACK_THE_BOT_LOGS)
            embed = discord.Embed(
                title=f"Participant joined",
                description=f"{member.mention} join {team_name}",
                color=int(config.EMBED_COLOR,16),
            )
            #embed.set_thumbnail(url=data["image"])
            await log_channel.send(embed=embed)
        else:
            await context.send(res['status'])

    @commands.command(name="removeMember")
    async def removeMember(self, context,member:discord.Member):
        """
            remove a member from a team
        """
        currentChannel = context.channel
        currentCategory = currentChannel.category
        #team_name = re.findall(r'(.*)_hackthebot$',currentChannel.name)
        user_id = context.author.id
        participant_id =  verify_api(user_id)
        print(participant_id)
        r =  requests.get(config.HACK_THE_BOT_URL+f"/api/participant/{participant_id}") 
        res = r.json()
        team_name = res['team']['name']
        print(team_name)
        if currentCategory.id in  config.HACK_THE_BOT_SPACES and  team_name !=None :
            await context.trigger_typing()
            user_id = context.author.id
            participant_id =verify_api(user_id)
            participant_id_to_delete =verify_api(member.id)
            r =  requests.delete(config.HACK_THE_BOT_URL+f"/api/participant/{participant_id}/team/remove",
                            json={"member":participant_id_to_delete}) 
            res = r.json()
            if res["status"] =='UNKNOWN_ERROR':
                raise HackTheBotUnknownError()
            elif res["status"] == 'SUCCESS':
                team_role = get(member.roles, name=f"{team_name}_hackthebot")
                await member.remove_roles(team_role)
                await context.send("Member removed from team successfully :white_check_mark:")
            else:
                await context.send(res['status'])

            
    

    
def setup(bot):
    bot.add_cog(hackthebot(bot))