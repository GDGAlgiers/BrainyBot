import os
import sys
import discord
from discord.ext import commands
from json import loads,dumps
from core.utils import send_embed, loads_to_object,verify_api
from core.errors import *
from discord.utils import get,find
import re,requests


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
        participant = verify_api(user_id)
        print
        # verify it is a participant and has no team 
        if participant["team"] !=None:
            embed = discord.Embed(
                title="Already have A team",
                description="You Already have a team :muscle:",
                color=int(config.EMBED_COLOR,16)
            )
            await context.author.send(embed=embed)
            return 
        await context.send("This command will allow you to create a new , "\
            "Please provide the required information once requested. If you would like to abort the creation, "\
            "do not respond and the program will time out.")
        time.sleep(1)
        await context.trigger_typing()

        ## get team name 
        await context.send("Please give us the team Name ! Team Name must be AlphaNumeric only [a-zA-Z0-9]  and length <25")
        try:
            team_name = await self.bot.wait_for('message', timeout=120, check=lambda message: message.author.id == context.message.author.id and message.content != "" )
            if len(team_name)> 25 or not re.match(r'[a-zA-Z0-9]+', team_name):
                raise HackTheBotInvalidTeamName()
        except asyncio.TimeoutError: 
            await send_embed(context, "Cancelled" ,":octagonal_sign: Command cancelled")
            await context.author.send("you took too long to provide the requested information.")
            return 
        
        ## get team image 
        time.sleep(1)
        await context.trigger_typing()
        await context.send("The team name has been set successfully now you can pass in an image that represent your team this step is tottaly optional ")



    @commands.dm_only()
    @commands.command(name="joinTeam")
    async def joinTeam(self, context,token:str):
        """
            Join a team using a token given to the team leader (the one who created the team)/
            team must contain at most 3 members
        """
        user_id = context.author.id
        await context.trigger_typing()
        participant_id = await verify_api(user_id)
        # verify it is a participant and has no team 
        

        r =  requests.post(config.HACK_THE_BOT_URL+f"/api/participant/{participant_id}/team/join",
                         json={"token":token}) 
        res = r.json()
        if res["status"] =='UNKNOWN_ERROR':
            raise HackTheBotUnknownError()
        elif res["status"] == 'SUCCESS':
            team_name = res["team_name"].lower()
            guild = self.bot.guilds[0] 
            team_role = get(guild.roles, name=f"{team_name}_hackthebot")
            member = find(lambda m:m.id == user_id,guild.members)
            await member.add_roles(team_role)
            await context.send(res['message'])
        else:
            await context.send(res['status'])


    @commands.command(name="removeMember")
    async def removeMember(self, context,member:discord.Member):
        """
            remove a member from a team
        """
        currentChannel = context.channel
        currentCategory = currentChannel.category
        team_name = re.findall(r'(.*)_hackthebot$',currentChannel.name)
        if currentCategory.id==int(config.HACKTHEBOT_CATEGORY_WORKSPACE_ID) and  team_name !=None :
            await context.trigger_typing()
            user_id = context.author.id
            participant_id = await verify_api(user_id)
            participant_id_to_delete = await verify_api(member.id)

            r =  requests.delete(config.HACK_THE_BOT_URL+f"/api/participant/{participant_id}/team/remove",
                            json={"member":participant_id_to_delete}) 
            res = r.json()
            if res["status"] =='UNKNOWN_ERROR':
                raise HackTheBotUnknownError()
            elif res["status"] == 'SUCCESS':
                team_role = get(member.roles, name=f"{team_name[0]}_hackthebot")
                await member.remove_roles(team_role)
                await context.send("Member deleted successfully")
            else:
                await context.send(res['status'])

            
    

    
def setup(bot):
    bot.add_cog(hackthebot(bot))