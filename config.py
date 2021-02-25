import datetime
import os
TOKEN = os.getenv("DISCORD_TOKEN")
# Can be multiple prefixes, like this: ("!", "?")
BOT_PREFIX = ("$")
OWNERS = [516805045199699969]
# Default cogs that I have created for the template
STARTUP_COGS = [
    "cogs.general", "cogs.help", "cogs.owner","cogs.mods", "cogs.hashcode", "cogs.fun"
]
MODERATOR_ROLE ="mod"
APPLICATION_ID = "803040512314966037"



############ HASHCODE PROPERTIES ###########
HASHCODE_LOGS_CHANNEL_ID = 810542408692400138
HASHCODE_CATEGORY_WORKSPACE_ID = 813213809455792169
HASHCODE_GENERAL_CHANNEL_ID = 810542408692400138
HASHCODE_CHECKIN_CHANNEL_ID = 810542871106945044


HASHCODE_START_DATE = datetime.datetime(2021, 2, 25, 17, 30, 0, 0)
HASHCODE_END_DATE = datetime.datetime(2021, 2, 25, 21, 30, 0, 0)
