import discord

async def getchannel(bot,id):
    channel = bot.get_channel(id)
    if not channel:
        try:
            channel = await bot.fetch_channel(id)
        except discord.InvalidData:
            channel = None
        except discord.HTTPException:
            channel = None
    return channel


async def getuser(bot,id):
    user = bot.get_user(id)

    if not user:
        user = await bot.fetch_user(id)

    return user

async def getguild(bot,id):
    guild = bot.get_guild(id)

    if not guild:
        guild = await bot.fetch_guild(id)

    return guild