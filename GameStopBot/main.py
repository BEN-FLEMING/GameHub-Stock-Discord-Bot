import discord
import requests
import os
import json
import datetime
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio

PREFIX = ("$")
bot = commands.Bot(command_prefix=PREFIX, description='Hi')

client = discord.Client()

test = datetime.datetime.now().replace(hour=20,minute=0,second=0,microsecond=0)
if datetime.datetime.now() < test:
    test = test - datetime.timedelta(days=1)

date_time = test.strftime("%Y-%m-%d %H:%M:%S")

def get_value():
  response = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=GME&interval=5min&apikey=" + os.getenv('API'))
  json_data = json.loads(response.text)
  datapoint = (json_data["Time Series (5min)"][date_time]['1. open'])
  return(datapoint)

@client.event 
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await client.change_presence(status=discord.Status.idle, activity=discord.Game("The Stonk Market"))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('$gmestock'):
    gmestock = get_value()
    await message.channel.send(gmestock)




client.run(os.getenv('TOKEN'))
