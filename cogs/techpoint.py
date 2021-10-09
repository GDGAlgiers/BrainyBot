import os
import sys
from datetime import date
import discord
from discord.ext import commands
from core.utils import upload_file_to_github, loads_to_object, send_embed
from core.markdown_utils import *

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    config = loads_to_object("config.json")

TOKEN = os.getenv('DISCORD_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPOSITORY_NAME = os.getenv('REPOSITORY_NAME')
BRANCH_NAME = os.getenv('BRANCH_NAME')
REPOSITORY_OWNER = os.getenv('REPOSITORY_OWNER')
FILES = {
    "tmp/notes.md" : "Notes",
    "tmp/resources.md" : "Resources",
    "tmp/off_notes.md" : "Off topic notes",
    "tmp/off_resources.md" : "Off topic resources"
    }

def _session_active():
    return os.path.isfile('tmp/'+str(date.today())+".md")


class Techpoint(commands.Cog, name="techpoint"):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role(config.MODERATOR_ROLE)  
    @commands.command(name="techpoint")
    async def techpoint(ctx, *, session_name):
        '''
        Launch a techpoint session, and enable taking notes and adding resources
        '''

        #Check if a session is already active
        if _session_active():
            await ctx.send("A session has already been launched!")
        else:
            #Create temp directory if it doesn't exist
            if not os.path.isdir('tmp'):
                os.mkdir('tmp')

            #Create the global file that will contain all the notes
            with open('tmp/'+str(date.today())+".md", "a") as file:
                file.write(h1("Techpoint : " + session_name)+'\n')
                file.write(h4(str(date.today()))+'\n')
            
            #create temporary file for each section
            for f in FILES:
                with open(f,"a") as file:
                    pass

            title = "Techpoint : " + session_name
            description = "Hello techpointers! enjoy your time and don't forget to take notes :) ! " 

            send_embed(ctx,title=title,description=description)

    @commands.command(name="note")
    async def note(ctx, *, note):
        '''
        Add a note to the current session
        '''
        if not _session_active():
            await ctx.send("A techpoint session must be active")
        else:
            with open("tmp/notes.md", "a") as file:
                file.write(list_item(note,ctx.author.name))

            await ctx.send("Note added!")
        
    @commands.command(name="onote")
    async def add_off_note(ctx, *, note):
        '''
        Add an off topic note to the current session
        '''
        if not _session_active():
            await ctx.send("A techpoint session must be active")
        else:
            with open("tmp/off_notes.md", "a") as file:
                file.write(list_item(note,ctx.author.name))

            await ctx.send("Off topic note added!")

    @commands.command(name="resource")
    async def add_resource(ctx, url, *, description):
        '''
        Add a resource to the current session
        '''
        if not _session_active():
            await ctx.send("A techpoint session must be active")
        else:
            with open("tmp/resources.md", "a") as file:
                file.write(list_item(link(description,url),ctx.author.name))

            await ctx.send("Resource added!")

    @commands.command(name="oresource")
    async def add_off_resource(ctx, url, *, description):
        '''
        Add an off topic resource to the current session
        '''
        if not _session_active():
            await ctx.send("A techpoint session must be active")
        else:
            with open("tmp/off_resources.md", "a") as file:
                file.write(list_item(link(description,url),ctx.author.name))

            await ctx.send("Off topic resource added!")

    @commands.has_role(config.MODERATOR_ROLE)  
    @commands.command(name="end")
    async def end_session(ctx):
        session_file = str(date.today())+".md"
        file_path = "tmp/"+session_file

        if not _session_active():
            await ctx.send("A techpoint session must be active")
        else:
            #Merge the content of the FILES
            with open(file_path, "a") as global_file:
                for file in FILES : 
                    with open(file, "r") as sub_file:
                        global_file.write(h2(FILES[file]) + '\n' + sub_file.read() + '\n')
                        os.remove(file)
            
            url = upload_file_to_github(file_path,session_file, REPOSITORY_NAME, REPOSITORY_OWNER, BRANCH_NAME, GITHUB_TOKEN)
            
            if(url != None):
                #Remove the file only if the upload is sucessful
                os.remove(file_path)
                await ctx.send("Session ended! Check it out here : " + url)
            else:
                await ctx.send("Something went wrong :(")


def setup(bot):
    bot.add_cog(Techpoint(bot))  