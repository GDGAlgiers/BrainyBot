"""
    This will hold the help command because we won't use the default help command
"""

import os
import sys
import discord
from discord.ext import commands
from core.utils import loads_to_object

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    config = loads_to_object("config.json")



class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.guild_only()
    @commands.command(name="help")
    async def help(self, context):
        """
        List all commands from every Cog the bot has loaded.
        """
        prefix = config.BOT_PREFIX

        embed = discord.Embed(
            title="Help", description="List of available commands:", color=int(config.EMBED_COLOR,16))
        # loop over all cogs
        for i in self.bot.cogs:
            # if the user is not an owner don't show owner commands
            if i.lower() =="owner" and context.message.author.id not in config.OWNERS:
                continue
            # if the user is not a mod don't show mod commands
            if i.lower() == "mod":
                role = discord.utils.find(lambda r: r.name == config.MODERATOR_ROLE, context.message.guild.roles)
                if role not in context.message.author.roles:
                    continue
            # else show cog commands
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            # get list of commands name
            command_list = [command.name for command in commands]
            # get description of each command
            command_description = [command.help for command in commands]
            # join all cogs command !
            help_text = '\n'.join(
                f'{prefix}{n} - {h}' for n, h in zip(command_list, command_description))
            embed.add_field(name=i.capitalize(),
                            value=f'```{help_text}```', inline=False)
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
