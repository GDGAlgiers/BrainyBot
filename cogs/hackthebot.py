import os
import sys
import discord
from discord.ext import commands
from json import loads,dumps
from core.utils import send_embed, loads_to_object
from core.errors import *


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
        async with self.bot.session.post(config.HACK_THE_BOT_URL+"/api/participant/verify", json={"discord_id":user_id}) as r:
            res = await r.json()
            if res["status"] =='UNAUTHORIZED':
                raise HackTheBotNotRegistered()
            elif res["status"] =='UNKNOWN_ERROR':
                raise HackTheBotUnknownError()
            elif res["status"] =='SUCCESS':
                print(res["participant"])
                embed = discord.Embed(
                    title="PARTICIPANT",
                    description="How can i help you **participant** :thinking: , You have registered **successfully** :white_check_mark:  Can't wait to say what you will made during the Hackathon :star_struck:",
                    color=int(config.EMBED_COLOR,16)
                )
                await context.author.send(embed=embed)
            else:
                raise HackTheBotUnknownError()
    

    
def setup(bot):
    bot.add_cog(hackthebot(bot))