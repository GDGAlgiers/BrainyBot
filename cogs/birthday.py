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
from core.firebase import *

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
                              description="""Hello challenger and welcome to our one and only “GDG Algiers’ 10th Birthday Challenge”.

I, Brainy :robot: will be your guide through this fun and entertaining journey, a little green companion along the way, at the end of our fellowship, you will have enough knowledge about GDG Algiers to go by, and I will have to disappear until our paths cross again.

The challenge will be a treasure hunt, meaning it’s a special code split into multiple parts, and being the generous bot that I am, I will help you move around.

As simple as it sounds, once you find a piece, use the `$hint [part_found]` command so that I can give you hints on the next parts.

If you get lucky enough to find the full code, try the `$validate [full_code]` to verify you really won or are still stuck with me for a few more rounds.

**Note:** Please don't share the code pieces you have found or else other challengers will steal your prizes.

**Another note:** For the first hint, you can try using the command `$hint` with no code.

Last thing to say, good luck, hero!
""",
                              title=f"GDG Algiers 10th Birthday challenge")
        embed.set_image(
            url="https://firebasestorage.googleapis.com/v0/b/gdg-wtm-website.appspot.com/o/Brainy-Utils%2Ftreasure.jpg?alt=media&token=7961b10e-f3ba-4c58-961c-983e53c9b718")
        startChallenge(ctx.author)
        await ctx.send(embed=embed)

    @commands.dm_only()
    @commands.command(brief="Verify Part Of the Code", description='Verify part of the code is correct and give hints on the next part')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hint(self, ctx, code: commands.clean_content(fix_channel_mentions=True) = None):
        """
            Verify the code part you have found and hint on the next $hint [code]
        """
        await ctx.trigger_typing()
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
        await ctx.trigger_typing()
        if code:
            if code not in parts:
                await send_embed(ctx, "Wrong Code part", "The code you have submitted is invalid ! I can't give you any hint")
                return
            else:
                part_number = parts.index(code)
                await send_embed(ctx, "Correct Code part", f"Congratulations you have found the part {part_number+1} of the code reply correctly to the next question to get hint about where to find the next part \n **Send Stop to stop the command**")
            await ctx.trigger_typing()
            await send_embed(ctx, "Question ", trivia[part_number+1]['question'])
            answer = None
            while True:
                try:
                    answer = await self.bot.wait_for('message', timeout=60, check=lambda message: message.author.id == ctx.message.author.id and message.content != "")
                    print(answer.content)
                    print(answer)
                    if answer.content == "Stop":
                        await send_embed(ctx, "", "Command Cancelled :x: ")
                        return
                    if answer.content.lower() in trivia[part_number+1]['answer']:
                        await ctx.trigger_typing()
                        # save log
                        submittedSuccessfully(ctx.author, code)
                        await send_embed(ctx, "Correct answer", trivia[part_number+1]['hint'])
                        break
                    else:
                        await ctx.trigger_typing()
                        await send_embed(ctx, "", "Wrong Answer :( ; Please try again\n **Send Stop to stop the command**")
                except asyncio.TimeoutError:
                    await ctx.trigger_typing()
                    await send_embed(ctx, "Cancelled", ":octagonal_sign: Command cancelled")
                    await ctx.author.send(" you took too long to provide the requested information.")
                    return

        else:
            await ctx.trigger_typing()
            await send_embed(ctx, "Question", "Here is your first hint, but wait reply to this question correctly first **"+trivia[0]['question']+"**")
            answer = None
            while True:
                try:
                    answer = await self.bot.wait_for('message', timeout=60, check=lambda message: message.author.id == ctx.message.author.id and message.content != "")
                    print(answer.content)
                    print(answer)
                    if answer.content == "Stop":
                        await send_embed(ctx, "", "Command Cancelled :x: ")
                        return
                    if answer.content.lower() in trivia[0]['answer']:
                        await ctx.trigger_typing()
                        submittedSuccessfully(ctx.author, None)
                        await send_embed(ctx, "Correct answer", trivia[0]['hint'])
                        break
                    else:
                        await ctx.trigger_typing()
                        await send_embed(ctx, "", "Wrong Answer :( ; Please try again\n **Send Stop to stop the command**")
                except asyncio.TimeoutError:
                    await ctx.trigger_typing()
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
        await ctx.trigger_typing()
        if "FULL_CODE" in os.environ:
            full_code = os.getenv("FULL_CODE")
        else:
            configJson = json.loads(open("config.json", "r").read())
            full_code = configJson["FULL_CODE"]
        validatedCode(ctx.author, code, code == full_code)
        if code != full_code:
            await send_embed(ctx, "Wrong Code part", "The code you have submitted is invalid ! Try again !! or contact and admin to get help")
            return
        else:
            await send_embed(ctx, "We have a winner", f"I can't believe that you have successfully found the hidden treasure well done adventurer I'm so proud of the path you have done, Here is your prize enjoy it https://forms.gle/YCCy2ujye6bBhMQQA")
            configJson = json.loads(open("config.json", "r").read())
            birthday_admins = configJson["BIRTHDAY_ADMINS"]
            for admin in birthday_admins:
                admin_user = await self.bot.fetch_user(admin)
                await send_embed(admin_user, "We have a winner", f"There is a winner who validated the full code {ctx.author.id}  {ctx.author.mention}  {ctx.author.name}")


def setup(bot):
    bot.add_cog(BirthDayChallenge(bot))
