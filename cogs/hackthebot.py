import os
import sys
import discord
from discord.ext import commands
from json import loads,dumps
from core.utils import send_embed, loads_to_object,verify_api
from core.errors import *
import re


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
        # verify it is a participant and has no team 
        if participant["team"] !=None:
            embed = discord.Embed(
                title="Already have A team",
                description="You Already have a team :muscle:",
                color=int(config.EMBED_COLOR,16)
            )
            await context.author.send(embed=embed)
            return 
        await ctx.send("This command will allow you to create a new , "\
            "Please provide the required information once requested. If you would like to abort the creation, "\
            "do not respond and the program will time out.")
        time.sleep(1)
        await ctx.trigger_typing()

        ## get team name 
        await ctx.send("Please give us the team Name ! Team Name must be AlphaNumeric only [a-zA-Z0-9]  and length <25")
        try:
            team_name = await self.bot.wait_for('message', timeout=120, check=lambda message: message.author.id == ctx.message.author.id and message.content != "" )
            if len(team_name)> 25 or not re.match(r'[a-zA-Z0-9]+', team_name):
                raise HackTheBotInvalidTeamName()
        except asyncio.TimeoutError: 
            await send_embed(ctx, "Cancelled" ,":octagonal_sign: Command cancelled")
            await ctx.author.send("you took too long to provide the requested information.")
            return 
        
        ## get team image 
        time.sleep(1)
        await ctx.trigger_typing()
        await ctx.send("The team name has been set successfully now you can pass in an image that represent your team this step is tottaly optional ")

        
            
    

    
def setup(bot):
    bot.add_cog(hackthebot(bot))