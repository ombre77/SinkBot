import discord
from discord.ext import commands
from discord import app_commands
import custom,colors
import json
import os
from PIL import Image
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


def channel_is_allowed(interaction: discord.Interaction, env_name: str) -> bool:
    channel_id_value = os.getenv(env_name)
    if not channel_id_value:
        return False
    try:
        allowed_channel = int(channel_id_value)
    except ValueError:
        return False
    return interaction.channel_id == allowed_channel


async def channel_denied_message(interaction: discord.Interaction, env_name: str) -> str:
    env_label = "WHEAT_BOT" if env_name == "WHEAT_BOT" else "SAND_BOT"
    interaction.response.send_message(f"This command can only be used in the {env_label} channel.",ephemeral=True)

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
    if not channel_is_allowed(interaction, "WHEAT_BOT"):
        await interaction.response.send_message(channel_denied_message(interaction, "WHEAT_BOT"), ephemeral=True)
        return
    custom.LogCommand.log(f"gow {level}",interaction.user)
    #load map
    file=custom.JSON_map("gow_costs.json")
    file.load()
    if level < 1 or level > len(file.map):
        await interaction.response.send_message("Not a valid level", ephemeral=True)
        return
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
    if not channel_is_allowed(interaction, "WHEAT_BOT"):
        await interaction.response.send_message(channel_denied_message(interaction, "WHEAT_BOT"), ephemeral=True)
        return
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
    if not await custom.MessageHelper.role_check(interaction,custom.MessageHelper.default_ops):
        return
    custom.LogCommand.log("announce",interaction.user)
    clr=custom.MessageHelper.COLOR_MAP.get(color,discord.Color.gold())
    embed=custom.Message(title,clr,f"{custom.MessageHelper.gamename()}-{custom.MessageHelper.version()}")
    embed.add_category("",message,bold=True)

    await interaction.response.send_message(embed=embed.render())

@bot.tree.command(name="setversion",description="Set the Wheat Game version")
async def setversion(interaction:discord.Interaction,new_version:str):
    if not await custom.MessageHelper.role_check(interaction,custom.MessageHelper.default_ops):
        return
    file=custom.JSON_map("./.game_infos.json")
    file.load()
    old=file.map["version"]
    custom.Json_set.path="./.game_infos.json"
    custom.Json_set.set("version",new_version)
    await interaction.response.send_message(f"Version has been set from {old} to {new_version}!",ephemeral=True)

@bot.tree.command(name="setname",description="Set the Wheat Game version name")
async def setversion(interaction:discord.Interaction,new_name:str):
    if not await custom.MessageHelper.role_check(interaction,custom.MessageHelper.default_ops):
        return
    file=custom.JSON_map("./.game_infos.json")
    file.load()
    old=file.map["name"]
    custom.Json_set.path="./.game_infos.json"
    custom.Json_set.set("name",new_name)
    await interaction.response.send_message(f"Version has been set from {old} to {new_name}!",ephemeral=True)

@bot.tree.command(name="kick")
async def kick(interaction:discord.Interaction):
    if not await custom.MessageHelper.role_check(interaction,custom.MessageHelper.default_ops):
        return
    await interaction.guild.leave()

@bot.tree.command(name="credits")
async def credits(interaction:discord.Interaction):
    file=custom.JSON_map("./credits.json")
    file.load()
    people:dict=file.map
    message=custom.Message("**Credits**",discord.Color.pink(),"Thanks to all those people for helping me creating this bot")
    for person in people:
        infos=people[person]
        display=infos["display"]
        display="`"+display+"`"
        roles:list=infos["roles"]
        roles=["- "+role for role in roles]
        str_content="\n".join(roles)
        message.add_category(display,str_content,bold=True)
    await interaction.response.send_message(embed=message.render())

@bot.tree.command(name="search",description="Search for a block wich name contains <name>")
async def search(interaction:discord.Interaction,name:str):
    if not channel_is_allowed(interaction, "SAND_BOT"):
        await interaction.response.send_message(channel_denied_message(interaction, "SAND_BOT"), ephemeral=True)
        return
    custom.LogCommand.log("search",interaction.user.name)
    file=custom.JSON_map("./doc_block.json")
    file.load()
    blocks=file.map
    potentials=[blocks[bk] for bk in blocks if name in bk]
    message=custom.Message(f"Results for '{name}':",discord.Colour.gold(),f"{len(potentials)} results")
    for potential in potentials:
        bk_name=potential["name"]
        desc=potential["desc"]
        message.add_category(f"- {bk_name}",desc,False)
    await interaction.response.send_message(embed=message.embed)

@bot.tree.command(name="what",description="Get infos on a SandSimu block")
async def what(interaction:discord.Interaction,name:str):
    if not channel_is_allowed(interaction, "SAND_BOT"):
        await channel_denied_message(interaction, "SAND_BOT")
        return
    custom.LogCommand.log("what",interaction.user.name)
    file=custom.JSON_map("./doc_block.json")
    file.load()
    blocks=file.map

    is_in=any(name==bk for bk in blocks)
    if not is_in:
        await interaction.response.send_message("Unknown block name. Try using /search maybe?",ephemeral=True)
        return
    
    block=blocks[name]
    bk_name=block["name"]
    pic=block["image"]
    desc=block["desc"]
    move=block["movement"]
    str_clr=block["color"]
    color=colors.COLOR_MAP[str_clr]

    special=block.get("special",False)

    message=custom.Message(bk_name,color,"")
    pic_path=f"./blocks/{pic}"
    if os.path.exists(pic_path):
        try:
            img=Image.open(pic_path)
            img=img.resize((256,256),Image.Resampling.NEAREST)
            img.save("temp.png")
            new_path="temp.png"
            message.embed.set_thumbnail(url=f"attachment://tumbnail.png")
            await interaction.response.send_message(embed=message.embed,file=discord.File(new_path,"tumbnail.png"))
            return
        except Exception:
            pass

    message.add_category(desc,"\n".join([f"- {"Else" if idx>0 else ""} {mov.lower() if idx>0 else mov}" for idx,mov in enumerate(move)]))
    if special:
        message.add_category("Special:","\n".join([f"- {spe}" for idx,spe in enumerate(special)]))
    await interaction.response.send_message(embed=message.render())

@bot.tree.command(name="addblock",description="Add a new block")
@app_commands.describe(
    movements="Separate very behaviour with ',' NO SPACES",
    special="Separate very behaviour with ',' NO SPACES"
)
async def addblock(interaction:discord.Interaction,name:str,display:str,image:str,desc:str,movements:str,color:str,special:str=None):
    if not await custom.MessageHelper.role_check(interaction,custom.MessageHelper.default_ops):
        return
    if not channel_is_allowed(interaction,"SAND_BOT"):
        await channel_denied_message(interaction,"SAND_BOT")
    custom.LogCommand.log(f"addblock > '{name}' '{display}' '{image}' '{desc}' '{movements}' '{color}' '{special}'",interaction.user.name)
    custom.Json_set.path="./doc_block.json"
    move=movements.split(",")
    if not color in colors.COLOR_MAP:
        await interaction.response.send_message("Unknown color",ephemeral=True)
        return
    dic={"name":display,"image":image,"desc":desc,"movement":move,"color":color}
    if special:
        dic["special"]=special.split(",")
    custom.Json_set.set(name,dic)
    await interaction.response.send_message("Block added!",ephemeral=True)

@bot.tree.command(name="delblock", description="Delete a block")
async def delblock(interaction: discord.Interaction, name: str):
    if not await custom.MessageHelper.role_check(interaction, custom.MessageHelper.default_ops):
        return
    if not channel_is_allowed(interaction, "SAND_BOT"):
        await channel_denied_message(interaction, "SAND_BOT")
        return
    file = custom.JSON_map("./doc_block.json")
    file.load()
    if name not in file.map:
        await interaction.response.send_message(f"Block `{name}` not found.", ephemeral=True)
        return
    del file.map[name]
    with open(file.path, "w") as f:
        json.dump({"map": file.map}, f, indent=4)
    await interaction.response.send_message(f"Block `{name}` deleted.", ephemeral=True)

@bot.tree.command(name="modblock", description="Modify a block field")
@app_commands.describe(
    name="Block key",
    category="Field to modify (name, image, desc, movement, color, special)",
    new_value="New value"
)
async def modblock(interaction: discord.Interaction, name: str, category: str, new_value: str):
    if not await custom.MessageHelper.role_check(interaction, ["Server Owner","Helpers","Bot helpers"]):
        return
    if not channel_is_allowed(interaction, "SAND_BOT"):
        await channel_denied_message(interaction, "SAND_BOT")
        return
    file = custom.JSON_map("./doc_block.json")
    file.load()
    block = file.map.get(name)
    if not block:
        await interaction.response.send_message(f"Block `{name}` not found.", ephemeral=True)
        return
    if category not in {"name", "image", "desc", "movement", "color", "special"}:
        await interaction.response.send_message(
            "Invalid category. Use: name, image, desc, movement, color, special",
            ephemeral=True
        )
        return
    if category in {"movement", "special"}:
        block[category] = [item.strip() for item in new_value.split(",") if item.strip()]
    else:
        block[category] = new_value
    with open(file.path, "w") as f:
        json.dump({"map": file.map}, f, indent=4)
    await interaction.response.send_message(
        f"Block `{name}` updated: `{category}` → `{new_value}`",
        ephemeral=True
    )

if __name__ == "__main__":
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot.run(TOKEN)