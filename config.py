import os
os.environ["DISCORD_TOKEN"]="ODMzNDUyODUxMDI4MDMzNTc3.YHyjdA.nyBs7raPP87wsmmF-W81X0Fo7qo"
TOKEN = os.getenv("DISCORD_TOKEN")
# Can be multiple prefixes, like this: ("!", "?")
BOT_PREFIX = ("$")
OWNERS = [268140405663465473]
# Default cogs that I have created for the template
STARTUP_COGS = [
    "cogs.general", "cogs.help", "cogs.owner","cogs.mods",  "cogs.fun", "cogs.techpoints"
]
MODERATOR_ROLE ="mod"
APPLICATION_ID = "803040512314966037"

