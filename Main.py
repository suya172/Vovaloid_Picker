from datetime import datetime, timedelta

import discord
import pytz
from discord.ext import tasks
from discord import app_commands
from discord.app_commands import describe

import Config as Config
from GenerateMessage import create_message
import asyncio
from typing import List, Union
import pickle

# Discordに関する設定
TOKEN: str = Config.TOKEN
DEBUG_CHANNEL_ID: int = int(Config.DEBUG_CHANNEL_ID)
intents = discord.Intents.default()
intents.messages = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# 送信時間
time_daily = '21:00'

history: List[str] = []
channels: List[int]  = []

# メッセージ送信用関数
async def sendMessage(message: str, channel: Union[int, None] = None):
    if channel is None:
        _c = 'all channels'
        for channel in channels:
            await client.get_channel(channel).send(message)
    else:
        _c = f'{channel}({client.get_channel(channel).name})'
        await client.get_channel(channel).send(message)
    await client.get_channel(DEBUG_CHANNEL_ID).send(f"Sent message to {_c}: {message}")


@tasks.loop(seconds=59)
async def checkTime():
    now = datetime.now(pytz.timezone('Asia/Tokyo')).strftime('%H:%M')
    if now == time_daily:
        await sendMessage(create_message())


@client.event
async def on_ready():
    print(f'起動しました。{(datetime.now() + timedelta(hours=9)).isoformat()}')
    await sendMessage('ｷﾄﾞｳｼﾏｼﾀ！')
    await client.change_presence(activity=discord.Game("今後千年草も生えない砂の惑星"))
    await tree.sync()
    await checkTime.start()

# コマンド
# チャンネルの登録・解除
@tree.command(name='register', description='メッセージを送信させたいチャンネルを登録します。既に登録されている場合は解除します。')
async def register(ctx: discord.Interaction):
    res:str = ''
    if ctx.channel.id in channels:
        channels.remove(ctx.channel.id)
        res = f'{ctx.channel.id}({ctx.channel.name}) を解除しました。'
    else:
        channels.append(ctx.channel.id)
        res = f'{ctx.channel.id}({ctx.channel.name}) を登録しました。'
    await ctx.response.send_message(res)
    with open('channels.pkl', 'wb') as f:
        pickle.dump(channels, f)

if __name__ == "__main__":
    with open('history.pkl', 'br') as f:
        history = pickle.load(f)
    with open('channels.pkl', 'br') as f:
        channels = pickle.load(f)

client.run(TOKEN)
