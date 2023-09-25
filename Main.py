import discord
from discord.ext import tasks
from datetime import datetime
from GenerateMessage import create_message
import Config
import asyncio

TOKEN=Config.TOKEN
CHANNEL_ID=int(Config.CHANNEL_ID)
intents=discord.Intents.all()

time_to_send='21:00'

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'起動しました。{datetime.now().isoformat()}')

async def SendMessage():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send(create_message())

@tasks.loop(seconds=60)
async def checkTime():
    now=datetime.now().strftime('%H:%M')
    if now == time_to_send:
        await SendMessage()

async def fn():
    await checkTime.start()

loop_ = asyncio.get_event_loop()
loop_.run_until_complete(fn())

client.run(TOKEN)
