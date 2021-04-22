import discord
from discord.ext import commands
import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

if not os.path.isfile("config.py"):
    sys.exit("'config.py' not found! Please add it and try again.")
else:
    import config


class mod(commands.Cog, name="mod"):
    '''Commands for moderators in a guild.'''

    def __init__(self, bot):
        self.bot = bot

    @commands.has_role(config.MODERATOR_ROLE)
    @commands.command(name="announce")
    async def announce(self, ctx, date: str = None, time: str = None, *, content: str = None):
        # async def announce(self, ctx, *, content: str = None):
        """
            Announce a message in a specific channel
        """

        def check(message):
            return message.author.id == ctx.message.author.id and message.content != ""

        # Get argument, convert them, Handling possible errors
        scheduled = False
        try:
            if date != None and time != None:
                # date format : year-month-day
                # time format : hour:minutes (doesn't work with AM,PM)
                postingTime = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
                if postingTime < datetime.now():
                    raise ValueError
                scheduled = True
            sent_initial_message = await ctx.send(
                "This command will allow you to post a message by Brainy , Please provide the required information once requested. If you would like to abort the creation, do not respond and the program will time out.")
            rl_object = {}
            cancelled = False
        except ValueError:
            await ctx.send("invalid arguments, try again.")
            cancelled = True

        if cancelled == False:
            error_messages = []
            user_messages = []
            sent_channel_message = await ctx.send("Mention the #channel where to announce the  message.")
            try:
                while True:
                    channel_message = await self.bot.wait_for('message', timeout=120, check=check)
                    if channel_message.channel_mentions:
                        rl_object["target_channel"] = channel_message.channel_mentions[0]
                        break
                    else:
                        error_messages.append((await ctx.send("The channel you mentioned is invalid.")))
            except asyncio.TimeoutError:
                await ctx.author.send(
                    "Message announcement creation failed, you took too long to provide the requested information.")
                cancelled = True
            finally:
                await sent_channel_message.delete()
                await sent_initial_message.delete()
                for message in error_messages:
                    await message.delete()

        if cancelled == False and 'target_channel' in rl_object:
            error_messages = []
            # Create a list of valid image formats for upload
            validfiles = [".jpg", ".jpeg", ".gif", ".png", ".bmp"]
            selector_embed = discord.Embed(
                title="Embed_title",
                description="Embed_content"
            )
            selector_embed.set_footer(text=f"Brainy Bot")
            sent_message_message = await ctx.send(
                "What would you like the message to say?\nFormatting is:"
                " `Message // Embed_title // Embed_content // Embed_color_in_hex`.\n\n`Embed_title`"
                ", `Embed_content` and `Embed_color_in_hex` are optional. You can type `none` in any"
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
                        if len(msg_values) > 3 and msg_values[3].lower() != "none":
                            selector_embed.color = int(msg_values[3], 16)
                    print(selector_embed)
                    # Prevent sending an empty embed instead of removing it
                    selector_embed = (
                        selector_embed
                        if selector_embed.title or selector_embed.description
                        else None
                    )
                    imageFile = None
                    if selector_msg_body or selector_embed:
                        target_channel = rl_object["target_channel"]
                        sent_final_message = None

                        try:
                            if len(message_message.attachments) > 0:
                                if message_message.attachments[0]:
                                    attachment = Path(message_message.attachments[0].filename)
                                    if attachment.suffix in validfiles:
                                        if not selector_embed == None:
                                            # send image within embed
                                            imageurl = message_message.attachments[0].url
                                            selector_embed.set_image(url=imageurl)
                                        else:
                                            # send Image without embed
                                            imageFile = await message_message.attachments[0].to_file()
                                    else:
                                        await message_message.delete()
                            if scheduled:
                                # wait until postTime come to post
                                timeToSleep = postingTime - datetime.now()
                                await asyncio.sleep(timeToSleep.total_seconds())
                            sent_final_message = await target_channel.send(
                                content=selector_msg_body, file=imageFile, embed=selector_embed
                            )
                            rl_object["message"] = dict(message_id=sent_final_message.id,
                                                        channel_id=sent_final_message.channel.id,
                                                        guild_id=sent_final_message.guild.id)
                            final_message = sent_final_message
                            break
                        except discord.Forbidden:
                            error_messages.append((await message.channel.send(
                                "I don't have permission to send messages to"
                                f" the channel {target_channel.mention}. Please check my permissions and try again."
                            )))
            except asyncio.TimeoutError:
                await ctx.author.send(
                    "Message  Anouncement creation failed, you took too long to provide the requested information.")
                cancelled = True
            finally:
                await sent_message_message.delete()
                for message in error_messages:
                    await message.delete()


def setup(bot):
    bot.add_cog(mod(bot))