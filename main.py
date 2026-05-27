import discord
from discord.ext import commands
from discord import app_commands
import custom
import json
import os
from dotenv import load_dotenv
if os.path.exists("./.env_priv"):
    load_dotenv(".env_priv")
else:
    load_dotenv(".env")

GUILD_IDS = [
    int(guild_id)
    for guild_id in os.getenv("GUILD_IDS", "").split(",")
    if guild_id
]

print(f"Guild(s): {GUILD_IDS}")

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

async def def_guild(id):
    guild=discord.Object(id=id)
    return guild

@bot.event
async def on_ready():
    for guild_id in GUILD_IDS:
        guild =await def_guild(guild_id)
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands to {guild_id}")

    synced = await bot.tree.sync(guild=guild)

    print(f"Synced {len(synced)} commands")
    print(f"Connected as {bot.user}")

@bot.tree.command(name="gow", description="GoW cost at each level")
async def gow(interaction: discord.Interaction,level:app_commands.Range[int,1,7]):
    custom.LogCommand.log(f"gow {level}",interaction.user)
    #load map
    file=custom.JSON_map("gow_costs.json")
    file.load()
    if level-1<0 or level-1>len(file.map):
        await interaction.response.send_message("Not a valid level")
    mapped:dict=file.map[level-1]
    trinkets=mapped.get("trinkets","Placeholder")
    strings=mapped.get("string","Placeholder")
    buff=mapped.get("desc","Placeholder")

    #message
    embed=custom.Message(f"Wheat Level {level}",discord.Color.gold(),buff)

    embed.add_category(name="Trinkets:", content=trinkets, inline=True)
    embed.add_category(name="Golden Strings:", content=strings, inline=True)

    await interaction.response.send_message(embed=embed.render())

@bot.tree.command(name="trinket", description="Give the price of trinkets")
async def trinkets(interaction: discord.Interaction,count:int):
    custom.LogCommand.log(f"trinket {count}",interaction.user)
    #load map
    file=custom.JSON_map("trinkets_costs.json")
    file.load()
    mapped:dict=file.map[0]
    haybales=mapped.get("haybales","Placeholder")
    wheat=mapped.get("wheat","Placeholder")

    haybales=int(haybales)*count
    wheat=int(wheat)*count

    if haybales>64:
        haybales=f"{haybales//64} stacks and {haybales%64} items"
    else:
        haybales=f"{haybales} items"
    if wheat>64:
        wheat=f"{wheat//64} stacks and {wheat%64} items"
    else:
        wheat=f"{wheat} items"

    #message
    embed=custom.Message(f"Trinket cost for {count} trinket(s)",discord.Color.gold())

    embed.add_category(name="Hay bales:", content=haybales)
    embed.add_category(name="Weaved wheats:", content=wheat)

    await interaction.response.send_message(embed=embed.render())

@bot.tree.command(name="announce",description="Make fancy announcements")
@app_commands.describe(
    title="Title",
    message="Content",
    color="Color code (examples: gold(default),red,yellow,..)"
)
async def announce(interaction:discord.Interaction,title:str,message:str,color:str="gold"):
    if not custom.MessageHelper.role_check(interaction,custom.MessageHelper.default_ops):
        return
    custom.LogCommand.log("announce",interaction.user)
    clr=custom.MessageHelper.COLOR_MAP.get(color,discord.Color.gold())
    embed=custom.Message(title,clr,f"{custom.MessageHelper.gamename()}-{custom.MessageHelper.version()}")
    embed.add_category("",message,bold=True)

    await interaction.response.send_message(embed=embed.render())

@bot.tree.command(name="setversion",description="Set the Wheat Game version")
async def setversion(interaction:discord.Interaction,new_version:str):
    if not custom.MessageHelper.role_check(interaction,custom.MessageHelper.default_ops):
        return
    file=custom.JSON_map("./.game_infos.json")
    file.load()
    old=file.map["version"]
    custom.Json_set.path="./.game_infos.json"
    custom.Json_set.set("version",new_version)
    await interaction.response.send_message(f"Version has been set from {old} to {new_version}!",ephemeral=True)

@bot.tree.command(name="setname",description="Set the Wheat Game version name")
async def setversion(interaction:discord.Interaction,new_name:str):
    if not custom.MessageHelper.role_check(interaction,custom.MessageHelper.default_ops):
        return
    file=custom.JSON_map("./.game_infos.json")
    file.load()
    old=file.map["name"]
    custom.Json_set.path="./.game_infos.json"
    custom.Json_set.set("name",new_name)
    await interaction.response.send_message(f"Version has been set from {old} to {new_name}!",ephemeral=True)

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(TOKEN)