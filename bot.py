import os
import discord
from discord.ext import commands
import requests

# Environment variables (set these before running)
HF_API_KEY = os.getenv("HF_API_KEY")       # e.g. hf_xxx
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") # your Discord bot token
MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"  # replace if desired

HF_API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def query_hf(prompt, max_tokens=512, temperature=0.7):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": max_tokens, "temperature": temperature},
    }
    r = requests.post(HF_API_URL, headers=headers, json=payload, timeout=120)
    if not r.ok:
        raise RuntimeError(f"HF API error {r.status_code}: {r.text}")
    data = r.json()
    if isinstance(data, list) and len(data) and "generated_text" in data[0]:
        return data[0]["generated_text"]
    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"]
    return str(data)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command(name="ask")
async def ask(ctx, *, prompt: str):
    """Use: !ask <your message>"""
    try:
        await ctx.send("💭 Thinking...")
        reply = query_hf(prompt)
        # Discord messages are limited to 2000 chars
        if len(reply) > 1900:
            reply = reply[:1900] + "\n...[truncated]"
        await ctx.send(reply)
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")

bot.run(DISCORD_TOKEN)
