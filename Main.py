import discord
from discord.ext import tasks,commands
from datetime import datetime
from GenerateMessage import create_message
import Config

TOKEN=Config.TOKEN
CHANNEL_ID=Config.CHANNEL_ID
intents=discord.Intents.all()

time_to_send='21:00'

client=discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'起動しました。{datetime.now().isoformat()}')

@tasks.loop(seconds=60)
async def loop():
    now=datetime.now().strftime('%H:%M')
    if now == time_to_send:
        channel = client.get_channel(CHANNEL_ID)
        message = create_message()
        await channel.send(message)


loop.start()

client.run(TOKEN)
