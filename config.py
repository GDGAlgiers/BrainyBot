import os
from json import dumps

if "DISCORD_TOKEN" in os.environ :
    TOKEN = os.getenv("DISCORD_TOKEN")
else:
    raise "Server token not found"

with open('spot.json','w+') as f:
    f.write(dumps(dict(spot=False)))

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


