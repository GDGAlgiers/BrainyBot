"""
    This is where we will have most of the fun commands 
"""
import os
import sys
import random
import json
import csv
import asyncio
import discord
from discord.ext import commands
import urllib
from core.utils import *

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    config = loads_to_object("config.json")


class BirthDayChallenge(commands.Cog, name="birthday"):
    def __init__(self, bot):
        self.bot = bot

    @commands.dm_only()
    @commands.command(brief="Join Challenge", description='Join the GDG Algiers 10th Birthday challenge')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def start(self, ctx):
        """ Join the GDG Algiers 10th Birthday challenge
         """

        await ctx.trigger_typing()

        embed = discord.Embed(color=0x00FF00,
                              description="""Hello Challenger :wave:
Welcome to our one and only 10th Birthday Challenge of GDG Algiers :partying_face:  I will be Brainy dir android mascot hna your guide through this fun and entertaining challenge :eyes:
The challenge will help you learn more information about GDG Algiers family and what they have done through the last 10 years :star_struck: 
The challenge will be a treasure hunt :map: Meaning, the treasure will be a special code split into multiple parts, and as a generous bot I will be the one guiding you to the treasure :relieved::man_detective: Once you find a part, use the  
`$check [code]` command so that I can give you hints on the next parts :grin: :heart:   
**Notice: ** For the first hint you can try using the command without code""",
                              title=f"GDG Algiers 10th Birthday challenge")
        embed.set_image(
            # https://firebasestorage.googleapis.com/v0/b/gdg-wtm-website.appspot.com/o/Brainy-Utils%2Ftreasure.jpg?alt=media&token=7961b10e-f3ba-4c58-961c-983e53c9b718
            url="https://firebasestorage.googleapis.com/v0/b/gdg-wtm-website.appspot.com/o/Brainy-Utils%2Ftreasure_hunt.jpg?alt=media&token=0efd6d62-85ce-4612-a9df-556e9a8661f8")
        await ctx.send(embed=embed)

    @commands.dm_only()
    @commands.command(brief="Verify Part Of the Code", description='Verify part of the code is correct and give hints on the next part')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def verify(self, ctx, code: commands.clean_content(fix_channel_mentions=True),):
        if "FULL_CODE" in os.environ:
            full_code = os.getenv("FULL_CODE")
        else:
            configJson = json.loads(open("config.json", "r").read())
            full_code = configJson["FULL_CODE"]
        code_len = len(full_code)
        part_len = len(full_code) // 5
        
        parts = [ full_code[ i:i+part_len ] for i in range(0,len(full_code),part_len) ]


        if "TRIVIA_QUESTIONS" in os.environ:
            questions = os.getenv("TRIVIA_QUESTIONS")
        else:
            response = urllib.request.urlopen(config.TRIVIA_QUESTIONS)
            trivia = json.loads(response.read())
        part_number= parts.index(code)
        await send_embed(ctx,"Question ",trivia[part_number]['question'])
        try:
            answer = await self.bot.wait_for('message', timeout=30)
        except asyncio.TimeoutError: 
                await send_embed(ctx, "Cancelled" ,":octagonal_sign: Command cancelled")
                await ctx.author.send("Message announcement creation failed, you took too long to provide the requested information.")
                return 
        if answer.content == trivia[part_number]['answer'] :
            await send_embed(ctx,"Hint",trivia[part_number]['hint'])
        else:
            await send_embed(ctx,"","Wrong Answer :(")


def setup(bot):
    bot.add_cog(BirthDayChallenge(bot))
