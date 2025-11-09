import os
import discord
from discord.ext import commands
import requests

# ---- Environment variables ----
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # Your Discord bot token
LOCAL_API_URL = os.getenv("LOCAL_API_URL", "http://localhost:8080/generate")

# ---- Discord client setup ----
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def query_local_api(prompt):
    """Send prompt to local Flask API and get model output"""
    r = requests.post(LOCAL_API_URL, json={"prompt": prompt})
    if r.status_code != 200:
        return f"Error: {r.text}"
    return r.json().get("text", "")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command(name="ask")
async def ask(ctx, *, prompt: str):
    """Use: !ask <your message>"""
    await ctx.send("💭 Thinking...")
    try:
        reply = query_local_api(prompt)
        if len(reply) > 1900:
            reply = reply[:1900] + "\n...[truncated]"
        await ctx.send(reply)
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

bot.run(DISCORD_TOKEN)
