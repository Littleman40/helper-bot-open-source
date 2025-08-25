# Discord Image Fix Bot
A Discord Bot that scans images uploaded to a channel, using OCR, and suggests fixes based on predefined rules. Built with Python, OpenAI and Discord.py
Was built to fix errors for No Hesi (assetto corsa server). 

*This project is not associated with, or endoresed by No Hesi LLC*

## Features
1. Transcribes images uploaded to a pretermined discord channel, using ChatGPT.
2. Matches these transcripts to "fix_rules.py" and/or "error_fixed.json".
3. If a match was found, it will respond with the error that was found + the preterminded fix.

## Prerequisites
Before installing, you’ll need:
Python 3.11+

### Discord Bot with the following:
Create at Discord Developer Portal
Add a bot → Copy the token
Enable Message Content Intent (required)
Invite bot to server with permissions:
* Read Messages/View Channels
* Send Messages
* Attach Files

### OpenAI API Key
Can be found at platform.openai.com

## Installation (Local)
Clone the repo:
```
git clone https://github.com/Littleman40/discord-bot.git
cd discord-bot
```
Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
Install dependencies:
```
pip install -r requirements.txt
```
Create a .env file in the project root:
```
DISCORD_BOT_TOKEN=your-bot-token-here
OPENAI_API_KEY=your-openai-key-here
```

Run the bot:
```
python app.py
```
## Deployment (Cloud + Docker)

Fork or clone this repo:
```
git clone https://github.com/Littleman40/discord-bot.git
cd discord-bot
```

Push the code to your own GitHub account (so your cloud platform can connect to it).

On your preferred cloud application platform:

1. Create a new Web Service

2. Select your forked GitHub repo

3. Set Environment = Docker

4. Add Environment Variables:
```
DISCORD_BOT_TOKEN=your-discord-bot-token

OPENAI_API_KEY=your-openai-api-key
```
Deploy the service.
The platform will automatically build and redeploy whenever you push updates to your GitHub repo.


# License
Copyright (c) 2025 Littleman40

Permission is granted to use, copy, modify, and share this code as long as proper credit is given to the original author.

You may not claim this work as your own or remove attribution.

This software is provided “as is”, without warranty of any kind.
