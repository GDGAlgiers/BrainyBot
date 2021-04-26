"""
    This cog contains techpoints commands... 
"""

import os
import sys
import json
import discord
from discord.ext import commands
if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


# This will define a cog named techpoints
class techpoints(commands.Cog, name="techpoints"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="suggest_topic", brief="suggest a topic", description='you can suggest a topic for the upcoming techpoints')
    async def suggest_topic (self, ctx, *args):
        """
        Suggest a topic for the upcoming techpoints.
        """
        if(ctx.author != config.APPLICATION_ID):
             with open('topics.json') as f:
                #await ctx.add_reaction("🧠")
                suggested_topics = json.load(f)
                new_topic=" ".join(args)
                if (new_topic in suggested_topics['suggested_topics']): return await ctx.channel.send("This topic has already been proposed")
                suggested_topics['suggested_topics'].append(new_topic)
                with open('topics.json','w') as f:
                    json.dump(suggested_topics,f,indent=7)
                await ctx.channel.send("Great one! New topic added to the list : " + new_topic)
    
    @commands.command(pass_context=True)
    async def topics_poll(self, ctx):
        """
        Make a topic poll, to choose the upcoming techpoint' theme
        """
        with open('topics.json') as f:
                suggested_topics = json.load(f)
        topics=suggested_topics['suggested_topics']
        if len(suggested_topics['suggested_topics']) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(suggested_topics['suggested_topics']) > 10:
            topics=suggested_topics['suggested_topics'] [0:10]
        reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(topics):
            description += '\n {} {} \n'.format(reactions[x], option)
        embed = discord.Embed(title="Choose one of these topics", description=''.join(description), color=0x00FF00)
        
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(topics)]:
            await react_message.add_reaction(reaction)
        #embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        #await react_message.edit_message(embed=embed)


def setup(bot):
    bot.add_cog(techpoints(bot))
