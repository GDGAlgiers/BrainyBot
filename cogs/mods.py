import discord
from discord.ext import commands
import asyncio
import os
import sys
import time
from pathlib import Path
from core.utils import loads_to_object,send_embed


if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    config = loads_to_object("config.json")

class Mod(commands.Cog,name="mod"):
    """
    Commands for moderators in a guild.
    """
    def __init__(self, bot):
        self.bot = bot


    @commands.has_role(config.MODERATOR_ROLE)     
    @commands.command(name="announce")
    async def announce(self, ctx, *, content: str=None):
        """
            Announce a message in a specific channel 
        """
        ##    Send informations about this command
        await ctx.trigger_typing()
        await ctx.send("This command will allow you to post a message by Brainy , "\
            "Please provide the required information once requested. If you would like to abort the creation, "\
            "do not respond and the program will time out.")
        time.sleep(1)
        await ctx.trigger_typing()
        await ctx.send("Mention the #channel where to announce the  message. or send STOP to cancel")
        announce_object = {}

        # wait until a valid channel is specified or cancel 
        while True:
            try:
                # wait for a message
                channel_message = await self.bot.wait_for('message', timeout=120, check=lambda message: message.author.id == ctx.message.author.id and message.content != "")
                if channel_message.channel_mentions:
                    announce_object["target_channel"] = channel_message.channel_mentions[0]
                    break
                elif channel_message.content == 'STOP':
                    await send_embed(ctx, "Cancelled" ,":octagonal_sign: Command cancelled")
                    return 
                else:
                    await ctx.send("The channel you mentioned is invalid. please send a valid #channel")
            except asyncio.TimeoutError: 
                await send_embed(ctx, "Cancelled" ,":octagonal_sign: Command cancelled")
                await ctx.author.send("Message announcement creation failed, you took too long to provide the requested information.")
                return 
        
        # specify extensions of image to validate its an image
        validfiles = [".jpg", ".jpeg", ".gif", ".png", ".bmp"]
        template_embed = discord.Embed(
            title="Embed_title",
            description="Embed_content"
        )
        template_embed.set_footer(text=f"Brainy Bot")

        # send the templating 
        sent_message_message = await ctx.send(
            "What would you like the message to say?\nFormatting is:"
            " `Message // Embed_title // Embed_content // Embed_color_in_hex`.\n\n`Embed_title`"
            ", `Embed_content` and `Embed_color_in_hex` are optional. You can type `none` in any"
            " of the argument fields above (e.g. `Embed_title`) to make the"
            " bot ignore it.\n\n\nMessage",
            embed=template_embed,
        )
        try:
            message_to_post = await self.bot.wait_for('message', timeout=120, check=lambda message: message.author.id == ctx.message.author.id and message.content != "")
            msg_values = message_to_post.content.split(" // ")
            
            # if nonce is specified then set body to None
            if msg_values[0].lower() != "none":
                post_body = msg_values[0]
            else:
                post_body =None

            post_embed = discord.Embed(colour=int(config.EMBED_COLOR, 16))
            post_embed.set_footer(text=f"Brainy Bot")

            if len(msg_values) > 1:
                if msg_values[1].lower() != "none":
                    post_embed.title = msg_values[1]
                if len(msg_values) > 2 and msg_values[2].lower() != "none":
                    post_embed.description = msg_values[2]


            # Prevent sending an empty embed instead of removing it
            if (not post_embed.title) and ( not post_embed.description) :
                post_embed = None

            if post_body or post_embed:
                target_channel = announce_object["target_channel"]
                # check if there is file attached to post 
                if len(message_to_post.attachments)>0:
                    attachment = Path(message_to_post.attachments[0].filename)
                    # verify its an image 
                    if attachment.suffix in validfiles:
                        imageurl = message_to_post.attachments[0].url
                        post_embed.set_image(url=imageurl)
                    else:
                        await send_embed(ctx, "Cancelled" ,"An invalid file attached :octagonal_sign: ")
                        return
                post = await target_channel.send(
                        content=post_body, embed=post_embed
                )
            else:
                await send_embed(ctx, "Cancelled" ,"Invalid Format passed :octagonal_sign: ")
                return 
        
        except asyncio.TimeoutError: 
                await send_embed(ctx, "Cancelled" ,":octagonal_sign: Command cancelled")
                await ctx.author.send("Message announcement creation failed, you took too long to provide the requested information.")
                return 

  

def setup(bot):
    bot.add_cog(Mod(bot))  