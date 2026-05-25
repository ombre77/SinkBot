import discord
from discord.ext import commands
from discord import app_commands
import json
import time

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
    
    def add_category(self,name:str,content:str,inline=True,bold=False):
        if bold:
            content=f"**{content}**"
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

class LogCommand:
    @classmethod
    def log(cls, name: str, user: str):
        now = time.localtime()

        day = now.tm_mday
        month = now.tm_mon         
        year = now.tm_year % 100  
        hour = now.tm_hour         
        minute = now.tm_min 
        second = now.tm_sec 

        print(f"[{day:02}/{month:02}/{year:02} {hour:02}:{minute:02}:{second:02}] User {user} issued command '{name}'")

class MessageHelper:
    COLOR_MAP = {
    "default": discord.Color.default(),
    "random": discord.Color.random(),

    "teal": discord.Color.teal(),
    "dark_teal": discord.Color.dark_teal(),

    "brand_green": discord.Color.brand_green(),
    "green": discord.Color.green(),
    "dark_green": discord.Color.dark_green(),

    "blue": discord.Color.blue(),
    "dark_blue": discord.Color.dark_blue(),

    "purple": discord.Color.purple(),
    "dark_purple": discord.Color.dark_purple(),

    "magenta": discord.Color.magenta(),

    "gold": discord.Color.gold(),
    "dark_gold": discord.Color.dark_gold(),

    "orange": discord.Color.orange(),
    "dark_orange": discord.Color.dark_orange(),

    "brand_red": discord.Color.brand_red(),
    "red": discord.Color.red(),
    "dark_red": discord.Color.dark_red(),

    "lighter_grey": discord.Color.lighter_grey(),
    "dark_grey": discord.Color.dark_grey(),
    "light_grey": discord.Color.light_grey(),
    "darker_grey": discord.Color.darker_grey(),

    "og_blurple": discord.Color.og_blurple(),
    "blurple": discord.Color.blurple(),
    "greyple": discord.Color.greyple(),

    "dark_theme": discord.Color.dark_theme(),
    "fuchsia": discord.Color.fuchsia(),
    "yellow": discord.Color.yellow(),
}
    @staticmethod
    async def role_check(interaction:discord.Interaction,role:str="Helpers"):
        is_role = discord.utils.get(
            interaction.user.roles,
            name=role
        )
        if is_role is None:
            await interaction.response.send_message("You do not have the permission required to execute this",ephemeral=True)
            return False
        return True
    
    @staticmethod
    def version():
        file=JSON_map("./.game_infos.json")
        file.load()
        map=file.map
        return map["version"]