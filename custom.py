import discord
from discord.ext import commands
from discord import app_commands
import json

class Message:
    def __init__(self,title:str,color:discord.Color,desc:str=None):
        self.title=title
        self.color=color
        self.desc=desc

        self.embed=discord.Embed(
            title=self.title,
            color=self.color,
            description=self.desc
        )
        self.footer("developed by Odysseus :3")
    
    def add_category(self,name:str,content:str,inline=True):
        self.embed.add_field(name=name,value=content,inline=inline)

    def footer(self,content:str):
        self.embed.set_footer(text=content)

    def render(self):
        return self.embed

class JSON_map:
    def __init__(self,path:str):
        self.path=path
        self.map={}
    
    def load(self):
        with open(self.path,"r") as f:
            file=json.load(f)
        self.map=file.get("map")
    