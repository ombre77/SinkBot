# **SinkBot**
![Logo](icon.png)

SinkBot is a discord bot designed for the Diamond Fire games **"Wheat Game"** and **Powder Simulation** discord server.
It provides game-related information with useful commands.

---

## Installation

### Requirements:
- **Python**
- **discord.py** (```pip install discord```)

### 1. Clone the repository

```bash
git clone https://github.com/OMBRE77/SinkBot.git
```
Or **download** the **zip** file and extract it.

### 2. Setup the bot

Create a `.env` file in the **SinkBot** folder with the following content:

```bash
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_server_id_here
WHEAT_BOT=your_channel_id_for_wheat_commands
SAND_BOT=your_channel_id_for_sand_commands
```

---

## Launch
Open a terminal in the **SinkBot** folder then type `python main.py` and let the file running. (You can of course **host** it on host site like **discloud** or **railway**)

---

## Features
### Commands
**Wheat commands**
- " **/gow [level]** " get the price and the buff of a specific **Gift of Wheat** level
- " **/trinkets [count]** " get the price of a certain amount of **trinkets**

**Sand commands**
- " **/search [name]** " search all blocks with *name* in their name
- " **/what [name]** " give infos on a block of the game
- " **/addblock [name] [display] [image] [desc] [color ]<[special]>** " Add a block to the block list
- " **/delblock [name]** " Del a block from the block list
- " **/modblock [name] [key] [new_value]** " Modifiy an element from a block of the block list
 
**Moderation commands**
- " **/announce [title] [message] ([color])** " send a pretty announcement

---
## Credits
- `_ody77_` > *Main dev*, *Github owner*, *Bot owner*
- `Slushyboy1212` > *Helper*, *Wiki creator*

**Contributors**
Thanks to all of you!
- `Finny`