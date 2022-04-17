import discord
import geocoder
import folium
import os

TOKEN = 'token' #copy token here

intents = discord.Intents().all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print('Bot ready')

@client.event
async def on_message(message):
  user_message = str(message.content)

  if message.author == client.user:
    return
    
  if '!locate' in user_message:
    address = None
    msg_string = user_message.split(' ')
    msg_string.remove('!locate')
    if len(msg_string) == 1:
      ip = msg_string[0]
    else:
      await message.channel.send('Invalid command')
      return
    g = geocoder.ip(ip)
    address = g.latlng
    if len(address) > 0:
      map = folium.Map(location=address, zoom_start=20)
      folium.Marker(location=address).add_to(map)
      map.save('map.html')
      await message.channel.send(file=discord.File(r'map.html'))
      os.remove('map.html')
      return
    else:
      await message.channel.send('Invalid IP')
      return

client.run(TOKEN)

#the command is !locate [ip]
