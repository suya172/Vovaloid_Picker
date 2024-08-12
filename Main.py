from datetime import datetime, timedelta

import discord
import pytz
from discord.ext import tasks

import Config
from GenerateMessage import create_message
import asyncio

TOKEN = Config.TOKEN
CHANNEL_ID = int(Config.CHANNEL_ID)
intents = discord.Intents.all()

time_to_send = '21:00'

client = discord.Client(intents=intents)


async def SendMessage():
    channel = client.get_channel(CHANNEL_ID)
    message = create_message()
    await channel.send(message)
    print(message)


@tasks.loop(seconds=30)
async def checkTime():
    now = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%H:%M')
    if now == time_to_send:
        await SendMessage()
        await asyncio.sleep(30)


@client.event
async def on_ready():
    print(f'起動しました。{(datetime.now() + timedelta(hours=9)).isoformat()}')
    await checkTime.start()

client.run(TOKEN)
