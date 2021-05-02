import os
from json import dumps,loads

configJson = loads(open("config.json","r").read())


os.environ["DISCORD_TOKEN"] = configJson["DISCORD_TOKEN"]

if "DISCORD_TOKEN" in os.environ :
    TOKEN = os.getenv("DISCORD_TOKEN")
else:
    raise "Server token not found"



# Can be multiple prefixes, like this: ("!", "?")
BOT_PREFIX = ("$")
OWNERS = [516805045199699969,642097099802017793]
# Default cogs that I have created for the template
STARTUP_COGS = [
    "cogs.general", "cogs.help", "cogs.owner","cogs.mods",  "cogs.fun"
]
MODERATOR_ROLE ="mod"
APPLICATION_ID = "803040512314966037"

COMANAGERS_IDs=[642097099802017793]

EMBED_COLOR = 0x00FF00


