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
`$hint [part_found]` command so that I can give you hints on the next parts :grin: :heart: If you were lucky enough to find the full code try the `$validate [full_code]` to verify you have the full code 
** Note ** Please don't share the parts you have found or else other challengers will steal your prizes :sad: 
**Notice: ** For the first hint you can try using the command without code""",
                              title=f"GDG Algiers 10th Birthday challenge")
        embed.set_image(
            # https://firebasestorage.googleapis.com/v0/b/gdg-wtm-website.appspot.com/o/Brainy-Utils%2Ftreasure.jpg?alt=media&token=7961b10e-f3ba-4c58-961c-983e53c9b718
            url="https://firebasestorage.googleapis.com/v0/b/gdg-wtm-website.appspot.com/o/Brainy-Utils%2Ftreasure_hunt.jpg?alt=media&token=0efd6d62-85ce-4612-a9df-556e9a8661f8")
        await ctx.send(embed=embed)

    @commands.dm_only()
    @commands.command(brief="Verify Part Of the Code", description='Verify part of the code is correct and give hints on the next part')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hint(self, ctx, code: commands.clean_content(fix_channel_mentions=True) = None):
        """
            Verify the code part you have found and hint on the next $hint [code]
        """
        if "FULL_CODE" in os.environ:
            full_code = os.getenv("FULL_CODE")
        else:
            configJson = json.loads(open("config.json", "r").read())
            full_code = configJson["FULL_CODE"]
        code_len = len(full_code)
        part_len = len(full_code) // 10
        parts = []
        for i in range(0, code_len, part_len):
            if len(full_code[i:i+part_len]) < part_len:
                parts[-1] = parts[-1] + full_code[i:i+part_len]
            else:
                parts.append(full_code[i:i+part_len])
        if "TRIVIA_QUESTIONS" in os.environ:
            response = urllib.request.urlopen(os.getenv("TRIVIA_QUESTIONS"))
            trivia = json.loads(response.read())
        else:
            configJson = json.loads(open("config.json", "r").read())
            response = urllib.request.urlopen(configJson['TRIVIA_QUESTIONS'])
            trivia = json.loads(response.read())
            
        if code:
            if code not in parts:
                await send_embed(ctx, "Wrong Code part", "The code you have submitted is invalid ! I can't give you any hint")
                return
            else:
                part_number = parts.index(code)
                await send_embed(ctx, "Correct Code part", f"Congratulations you have found the part {part_number+1} of the code reply correctly to the next question to get hint about where to find the next part")

            await send_embed(ctx, "Question ", trivia[part_number+1]['question'])
            answer = None
            while True:
                try:
                    answer = await self.bot.wait_for('message', timeout=60, check=lambda message: message.content != "")
                    print(answer.content)
                    print(answer)
                    if answer.content.lower() in trivia[part_number+1]['answer']:
                        await send_embed(ctx, "Correct answer", trivia[part_number+1]['hint'])
                        break
                    else:
                        await send_embed(ctx, "", "Wrong Answer :( ; Please try again")
                except asyncio.TimeoutError:
                    await send_embed(ctx, "Cancelled", ":octagonal_sign: Command cancelled")
                    await ctx.author.send(" you took too long to provide the requested information.")
                    return

        else:
            await send_embed(ctx, "Question", "Here is your first hint, but wait reply to this question correctly first **"+trivia[0]['question']+"**")
            answer = None
            while True:
                try:
                    answer = await self.bot.wait_for('message', timeout=30)
                    print(answer.content)
                    print(answer)
                    if answer.content == trivia[0]['answer']:
                        await send_embed(ctx, "Hint", trivia[0]['hint'])
                        break
                    else:
                        await send_embed(ctx, "", "Wrong Answer :( ; Please try again")
                except asyncio.TimeoutError:
                    await send_embed(ctx, "Cancelled", ":octagonal_sign: Command cancelled")
                    await ctx.author.send(" you took too long to provide the requested information.")
                    return

    @commands.dm_only()
    @commands.command(brief="Validate the full code", description='Send the code to brainy and he will validate it and send you your prize!')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def validate(self, ctx, code: commands.clean_content(fix_channel_mentions=True),):
        """
            Send the code to brainy and he will validate it and send you your prize!
        """

        if "FULL_CODE" in os.environ:
            full_code = os.getenv("FULL_CODE")
        else:
            configJson = json.loads(open("config.json", "r").read())
            full_code = configJson["FULL_CODE"]

        if code != full_code:
            await send_embed(ctx, "Wrong Code part", "The code you have submitted is invalid ! Try again !! or contact and admin to get help")
            return
        else:
            await send_embed(ctx, "We have a winner", f"I can't believe that you have successfully found the hidden treasure well done adventurer I'm so proud of the path you have done, Here is your prize enjoy it https://forms.gle/YCCy2ujye6bBhMQQA")


def setup(bot):
    bot.add_cog(BirthDayChallenge(bot))
