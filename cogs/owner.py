import os
import sys
import discord
import asyncio
from core.db import  db
from discord.ext import commands

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


class owner(commands.Cog, name="owner"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="shutdown")
    async def shutdown(self, context):
        """
        Make the bot shutdown
        """
        if context.message.author.id in config.OWNERS:
            embed = discord.Embed(
                description="Shutting down. Bye! :wave:",
                color=0x00FF00
            )
            await context.send(embed=embed)
            await self.bot.logout()
            await self.bot.close()
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0x00FF00
            )
            await context.send(embed=embed)

    @commands.command(name="say", aliases=["echo"])
    async def say(self, context, *, args):
        """
        The bot will say anything you want.
        """
        if context.message.author.id in config.OWNERS:
            await context.send(args)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0x00FF00
            )
            await context.send(embed=embed)

    @commands.command(name="embed")
    async def embed(self, context, *, args):
        """
        The bot will say anything you want, but within embeds.
        """
        if context.message.author.id in config.OWNERS:
            embed = discord.Embed(
                description=args,
                color=0x00FF00
            )
            await context.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error!",
                description="You don't have the permission to use this command.",
                color=0x00FF00
            )
            await context.send(embed=embed)
    @commands.command(name="new", aliases=['create'])
    async def new(self, ctx):
        """
        Create a new message to self assign roles 
        """

        if ctx.message.author.id in config.OWNERS:
            sent_initial_message = await ctx.send("This command will allow you to create a self assigned message role, Please provide the required information once requested. If you would like to abort the creation, do not respond and the program will time out.")
            rl_object = {}
            cancelled = False
            async def getchannel(id):
                channel = self.bot.get_channel(id)

                if not channel:
                    try:
                        channel = await self.bot.fetch_channel(id)
                    except discord.InvalidData:
                        channel = None
                    except discord.HTTPException:
                        channel = None

                return channel

            def check(message):
                return message.author.id == ctx.message.author.id and message.content != ""

            if cancelled == False:
                error_messages = []
                user_messages = []
                sent_reactions_message = await ctx.send(
                        "Attach roles and emojis separated by one space (one combination"
                        " per message). When you are done type `done`. Example:\n:smile:"
                        " `@Role`"
                )
                rl_object["reactions"] = {}
                try:
                    while True:
                        reactions_message = await self.bot.wait_for('message', timeout=120, check=check)
                        user_messages.append(reactions_message)
                        if reactions_message.content.lower() != "done":
                            reaction = (reactions_message.content.split())[0]
                            try:
                                role = reactions_message.role_mentions[0].id
                            except IndexError:
                                error_messages.append((await ctx.send(
                                    "Mention a role after the reaction. Example:\n:smile:"
                                    " `@Role`"
                                )))
                                continue

                            if reaction in rl_object["reactions"]:
                                error_messages.append((await ctx.send(
                                    "You have already used that reaction for another role. Please choose another reaction"
                                )))
                                continue
                            else:
                                try:
                                    await reactions_message.add_reaction(reaction)
                                    rl_object["reactions"][reaction] = role
                                except discord.HTTPException:
                                    error_messages.append((await ctx.send(
                                        "You can only use reactions uploaded to servers the bot has"
                                        " access to or standard emojis."
                                    )))
                                    continue
                        else:
                            break
                except asyncio.TimeoutError:
                    await ctx.author.send("Self Assigned role creation failed, you took too long to provide the requested information.")
                    cancelled = True
                finally:
                    await sent_reactions_message.delete()
                    for message in error_messages + user_messages:
                        await message.delete()

            if cancelled == False:
                sent_oldmessagequestion_message = await ctx.send(f"Would you like to use an existing message or create one using {self.bot.user.mention}? Please react with a 🗨️ to use an existing message or a 🤖 to create one.")
                def reaction_check(payload):
                    return payload.member.id == ctx.message.author.id and payload.message_id == sent_oldmessagequestion_message.id and (str(payload.emoji) == "🗨️" or str(payload.emoji) == "🤖")
                try:
                    await sent_oldmessagequestion_message.add_reaction("🗨️")
                    await sent_oldmessagequestion_message.add_reaction("🤖")
                    oldmessagequestion_response_payload = await self.bot.wait_for('raw_reaction_add', timeout=120, check=reaction_check)

                    if str(oldmessagequestion_response_payload.emoji) == "🗨️":
                        rl_object["old_message"] = True
                    else:
                        rl_object["old_message"] = False
                except asyncio.TimeoutError:
                    await ctx.author.send("Self assigned role creation failed, you took too long to provide the requested information.")
                    cancelled = True
                finally:
                    await sent_oldmessagequestion_message.delete()
            if cancelled == False:
                error_messages = []
                user_messages = []
                if rl_object["old_message"] == True:
                    sent_oldmessage_message = await ctx.send(f"Which message would you like to use? Please react with a 🔧 on the message you would like to use.")
                    def reaction_check2(payload):
                        return payload.member.id == ctx.message.author.id and payload.guild_id == sent_oldmessage_message.guild.id and str(payload.emoji) == "🔧"
                    try:
                        while True:
                            oldmessage_response_payload = await self.bot.wait_for('raw_reaction_add', timeout=120, check=reaction_check2)
                            try:
                                channel = await getchannel(oldmessage_response_payload.channel_id)
                                if channel is None:
                                    raise discord.NotFound
                                try:
                                    message = await channel.fetch_message(oldmessage_response_payload.message_id)
                                except discord.HTTPException:
                                    raise discord.NotFound
                                try:
                                    await message.add_reaction("👌")
                                    await message.remove_reaction("👌", message.guild.me)
                                    await message.remove_reaction("🔧", ctx.author)
                                except discord.HTTPException:
                                    raise discord.NotFound
                                if db.exists(message.id):
                                    raise ValueError
                                rl_object["message"] = dict(message_id=message.id, channel_id=message.channel.id, guild_id=message.guild.id)
                                final_message = message
                                break
                            except discord.NotFound:
                                error_messages.append((await ctx.send("I can not access or add reactions to the requested message. Do I have sufficent permissions?")))
                            except ValueError:
                                error_messages.append((await ctx.send(f"This message already got a Self assigned role instance attached to it, consider running `edit` instead.")))
                    except asyncio.TimeoutError:
                        await ctx.author.send("Self assigned role creation failed, you took too long to provide the requested information.")
                        cancelled = True
                    finally:
                        await sent_oldmessage_message.delete()
                        for message in error_messages:
                            await message.delete()
                else:
                    sent_channel_message = await ctx.send("Mention the #channel where to send the auto-role message.")
                    try:
                        while True:
                            channel_message = await self.bot.wait_for('message', timeout=120, check=check)
                            if channel_message.channel_mentions:
                                rl_object["target_channel"] = channel_message.channel_mentions[0]
                                break
                            else:
                                error_messages.append((await message.channel.send("The channel you mentioned is invalid.")))
                    except asyncio.TimeoutError: 
                        await ctx.author.send("Self assigned role creation failed, you took too long to provide the requested information.")
                        cancelled = True
                    finally:
                        await sent_channel_message.delete()
                        for message in error_messages:
                            await message.delete()
            if cancelled == False and 'target_channel' in rl_object:
                error_messages = []
                selector_embed = discord.Embed(
                    title="Embed_title",
                    description="Embed_content",
                    color=0x00FF00
                )
                selector_embed.set_footer(text=f"Brainy Bot")

                sent_message_message = await message.channel.send(
                    "What would you like the message to say?\nFormatting is:"
                    " `Message // Embed_title // Embed_content`.\n\n`Embed_title`"
                    " and `Embed_content` are optional. You can type `none` in any"
                    " of the argument fields above (e.g. `Embed_title`) to make the"
                    " bot ignore it.\n\n\nMessage",
                    embed=selector_embed,
                )
                try:
                    while True:
                        message_message = await self.bot.wait_for('message', timeout=120, check=check)
                        # I would usually end up deleting message_message in the end but users usually want to be able to access the 
                        # format they once used incase they want to make any minor changes
                        msg_values = message_message.content.split(" // ")
                        # This whole system could also be re-done using wait_for to make the syntax easier for the user
                        # But it would be a breaking change that would be annoying for thoose who have saved their message commands
                        # for editing.
                        selector_msg_body = (
                            msg_values[0] if msg_values[0].lower() != "none" else None
                        )
                        selector_embed = discord.Embed(colour=0x00FF00)
                        selector_embed.set_footer(text=f"Brainy Bot")

                        if len(msg_values) > 1:
                            if msg_values[1].lower() != "none":
                                selector_embed.title = msg_values[1]
                            if len(msg_values) > 2 and msg_values[2].lower() != "none":
                                selector_embed.description = msg_values[2]

                        # Prevent sending an empty embed instead of removing it
                        selector_embed = (
                            selector_embed
                            if selector_embed.title or selector_embed.description
                            else None
                        )

                        if selector_msg_body or selector_embed:
                            target_channel = rl_object["target_channel"]
                            sent_final_message = None
                            try:
                                sent_final_message = await target_channel.send(
                                    content=selector_msg_body, embed=selector_embed
                                )
                                rl_object["message"] = dict(message_id=sent_final_message.id, channel_id=sent_final_message.channel.id, guild_id=sent_final_message.guild.id)
                                final_message = sent_final_message
                                break
                            except discord.Forbidden:
                                error_messages.append((await message.channel.send(
                                    "I don't have permission to send messages to"
                                    f" the channel {target_channel.mention}. Please check my permissions and try again."
                                )))
                except asyncio.TimeoutError:
                    await ctx.author.send("Self assigned role creation failed, you took too long to provide the requested information.")
                    cancelled = True
                finally:
                    await sent_message_message.delete()
                    for message in error_messages:
                        await message.delete()
            if cancelled == False:
                 # Ait we are (almost) all done, now we just need to insert that into the database and add the reactions 💪
                try:
                    r = db.add_reaction_role(rl_object)
                except Exception:
                    await ctx.send(f"The requested message already got a reaction light instance attached to it, consider running `{prefix}edit` instead.")
                    return

                if isinstance(r, Exception):
                    await print(
                        ctx.message.guild.id,
                        f"Database error when creating reaction-light instance:\n```\n{r}\n```",
                    )
                    return
                for reaction, _ in rl_object["reactions"].items():
                    await final_message.add_reaction(reaction)
                await ctx.message.add_reaction("✅")
            await sent_initial_message.delete()
            if cancelled == True:
                await ctx.message.add_reaction("❌")
        else:
            await ctx.send("You do not have an admin role.")


def setup(bot):
    bot.add_cog(owner(bot))
