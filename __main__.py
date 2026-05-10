import discord
from discord.ext import commands
from discord import app_commands
import custom
import json
import os
from dotenv import load_dotenv

load_dotenv()
GUILD_ID = os.getenv("GUILD_ID")

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)

    bot.tree.clear_commands(guild=guild)

    bot.tree.copy_global_to(guild=guild)

    synced = await bot.tree.sync(guild=guild)

    print(f"Synced {len(synced)} commands")
    print(f"Connected as {bot.user}")

@bot.tree.command(name="gow", description="GoW cost at each level")
async def gow(interaction: discord.Interaction,level:app_commands.Range[int,1,7]):
    #load map
    file=custom.JSON_map("gow_costs.json")
    file.load()
    if level-1<0 or level-1>len(map):
        await interaction.response.send_message("Not a valid level")
    mapped:dict=file.map[level-1]
    trinkets=mapped.get("trinkets","Placeholder")
    strings=mapped.get("string","Placeholder")
    buff=mapped.get("desc","Placeholder")

    #message
    embed=custom.Message(f"Wheat Level {level}")

    embed.add_category(name="Trinkets:", content=trinkets, inline=True)
    embed.add_category(name="Golden Strings:", content=strings, inline=True)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="trinket", description="Give the price of trinkets")
async def gow(interaction: discord.Interaction,count:int):
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

    await interaction.response.send_message(embed=embed)

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(TOKEN)