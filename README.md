# WheatBot
![Logo](icon.png)

WheatBot is a Discord bot designed for the Diamond Fire game **"Wheat Game"** discord server.
It provides game-related information with the commands "/trinkets" and "/gow" (and others are coming in the future)

---

## Installation

### Requirements:
- **Python**
- **discord.py** (```pip install discord```)

### 1. Clone the repository

```bash
git clone https://github.com/OMBRE77/WheatBot.git
cd WheatBot
```
Or **download** the **zip** file and extract it.

### 2. Setup the bot

Create a `.env` file in the **WheatBot** folder with the following content:

```
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_server_id_here
```

---

## Launch
Open a terminal in the **WheatBot** folder then type `python .` and let the file running. (You can of course **host** it on host site like **discloud** or **railway**)

---

## Features
### Commands
- " **/gow [level]** " get the price and the buff of a specific **Gift of Wheat** level
- " **/trinkets [count]** " get the price of a certain amount of **trinkets**
- " **/announce [title] [message] ([color])** " send a pretty announcement