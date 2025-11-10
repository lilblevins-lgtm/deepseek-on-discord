import os
import discord
from discord.ext import commands
import requests

DISCORD_TOKEN = os.getenv("MTQzNzIxMjc1NTE0Nzg4NjY3Mg.G7PzO9.V7JP9DAcep0MNcZUpZ85C8Zl3vli5qNgvzmV5U")
LOCAL_API_URL = os.getenv("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", "http://localhost:8080/generate")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def query_local_api(prompt):
    try:
        r = requests.post(LOCAL_API_URL, json={"prompt": prompt})
        r.raise_for_status()
        return r.json().get("text", "")
    except Exception as e:
        return f"API Error: {e}"

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command(name="ask")
async def ask(ctx, *, prompt: str):
    await ctx.send("💭 Thinking...")
    reply = query_local_api(prompt)
    await ctx.send(reply[:1900] + ("..." if len(reply) > 1900 else ""))

bot.run(DISCORD_TOKEN)
