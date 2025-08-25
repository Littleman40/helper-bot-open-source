# -*- coding: utf-8 -*-
import os, io, base64, json, re, time, logging, discord, openai
from dotenv import load_dotenv
from PIL import Image
from discord.ext import commands
from discord.utils import escape_mentions
from fix_rules import get_fix

openai.api_key = os.getenv("OPENAI_API_KEY")


logging.basicConfig(
    filename='bot.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s'
)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# YOU MUST REPLACE THESE CHANNEL ID's!!
HELP_CHANNEL_ID = 1398853130753671238
TRANSCRIPT_CHANNEL_ID = 1398851513903747122
UPDATES_CHANNEL_ID = 1398860479644041256 

# You can apply a custom rate limit per person
USER_COOLDOWN = 10
last_request = {}

# Max file size
MAX_FILE_SIZE = 4 * 1024 * 1024

def encode_image(b): return base64.b64encode(b).decode('utf-8')

def send_image_to_gpt(b):
    base64_image = encode_image(b)
    
    try:
        resp = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Read this image exactly as shown and extract the full text of any and all messages that may indicate an error, issue, system notice, loading state, or unusual output. Return the exact wording without interpretation or formatting. If the image does not contain any such message, reply with: No error-related messages found. Do not speculate or add any commentary. Only perform this extraction task."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]
            }],
            max_tokens=1000
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return None

def match_fix(extracted_text):
    return get_fix(extracted_text)

def increment_version_string(version):
    major, minor, patch = map(int, version.split("."))
    patch += 1
    return f"{major}.{minor}.{str(patch).zfill(2)}"

@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user.name}")
    updates_channel = bot.get_channel(UPDATES_CHANNEL_ID)
    if updates_channel:
        async for msg in updates_channel.history(limit=100):
            match = re.search(r"version (\d+\.\d+\.\d+)", msg.content)
            if match:
                last_version = match.group(1)
                new_version = increment_version_string(last_version)
                itemFixed = "ENTER UPDATE HERE"
                await updates_channel.send(f"## Bot updated to version {new_version}\n**What was updated**: {itemFixed}")
                return
        await updates_channel.send("Bot updated to version 0.1.01")

@bot.event
async def on_message(msg):
    # Ignoring other bots or non help channel's
    if msg.author.bot or msg.channel.id != HELP_CHANNEL_ID:
        return

    now = time.time()
    last = last_request.get(msg.author.id, 0)
    if now - last < USER_COOLDOWN:
        return
    last_request[msg.author.id] = now

    for att in msg.attachments:
        if not att.filename.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        if att.size > MAX_FILE_SIZE:
            transcript = bot.get_channel(TRANSCRIPT_CHANNEL_ID)
            if transcript:
                await transcript.send(f"File from {msg.author.mention} too large ({att.size} bytes)")
            continue

        async with msg.channel.typing():
            try:
                raw = await att.read()
                Image.open(io.BytesIO(raw))
            except Exception as e:
                logging.warning(f"Invalid image from {msg.author.id}: {e}")
                continue

            extracted = send_image_to_gpt(raw)
            if not extracted:
                transcript = bot.get_channel(TRANSCRIPT_CHANNEL_ID)
                if transcript:
                    await transcript.send(f"Error processing image from {msg.author.mention}")
                continue

            if extracted.startswith("```") and extracted.endswith("```"):
                extracted = extracted[3:-3].strip()
            extracted = escape_mentions(extracted)

            transcript = bot.get_channel(TRANSCRIPT_CHANNEL_ID)
            if transcript:
                file = discord.File(io.BytesIO(raw), filename=att.filename)
                await transcript.send(
                    content=f"**Transcript from {msg.author.mention}**\n```{extracted[:1900]}```",
                    file=file
                )

            fix = get_fix(extracted)
            if fix:
                await msg.reply(escape_mentions(fix))
                logging.info(f"Replied fix to {msg.author.id}")

    await bot.process_commands(msg)

bot.run(os.getenv("DISCORD_BOT_TOKEN"))
