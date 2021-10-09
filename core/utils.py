import discord
from collections.abc import Sequence
import json
import os
import requests
from types import SimpleNamespace
import sys
from core.errors import *
import base64
import requests
import json


def loads_to_object(json_file):
    """
        Loads from a json file  to a python object filling its properties with 
        dictionnary key 
    """
    return json.loads(open(json_file, "r").read(), object_hook=lambda d: SimpleNamespace(**d))


if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    config = loads_to_object("config.json")


async def getchannel(bot, id):
    channel = bot.get_channel(id)
    if not channel:
        try:
            channel = await bot.fetch_channel(id)
        except discord.InvalidData:
            channel = None
        except discord.HTTPException:
            channel = None
    return channel


async def getuser(bot, id):
    user = bot.get_user(id)

    if not user:
        user = await bot.fetch_user(id)

    return user


async def getguild(bot, id):
    guild = bot.get_guild(id)

    if not guild:
        guild = await bot.fetch_guild(id)

    return guild


async def send_embed(context, title, description, color=int(config.EMBED_COLOR, 16)):
    embed = discord.Embed(
        title=title,
        description=description,
        color=color
    )
    await context.send(embed=embed)


def upload_file_to_github(file_path, file_name, repo_name, owner,  branch_name, token):
    url = "https://api.github.com/repos/"+owner+'/'+repo_name+"/contents/"+file_name

    headers = {
        "Authorization": "token " + token,
        "Accept": "application/vnd.github.v3.raw",
        "Content-Type": "application/json"
    }

    with open(file_path, "rb") as file:
        data = {
            "message": "Uploaded " + file_name + " to " + branch_name,
            "content": base64.b64encode(file.read()).decode("utf-8")
        }

    response = requests.put(url, data=json.dumps(data), headers=headers)

    if response.status_code == 201:
        return response.json()["content"]["html_url"]
    else:
        return None
