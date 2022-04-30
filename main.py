import discord
import geocoder
import folium
import os
from html2image import Html2Image

TOKEN = 'token' #copy token here

hti = Html2Image(
  custom_flags=['--virtual-time-budget=1000']
)

intents = discord.Intents().all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print('Bot ready')

@client.event
async def on_message(message):
  user_message = str(message.content)
    
  if '$locate' in user_message:
    address = None
    msg_string = user_message.split(' ')
    msg_string.remove('$locate')
    if len(msg_string) == 2:
      ip = msg_string[0]
      zoom_str = msg_string[1]
      try:
        zoom = int(zoom_str[5:])
      except:
        await message.channel.send('Invalid command')
        return
    elif len(msg_string) == 1:
      ip = msg_string[0]
      zoom=12
    else:
      await message.channel.send('Invalid command')
      return
    g = geocoder.ip(ip)
    address = g.latlng
    if len(address) > 0:
      map = folium.Map(location=address, zoom_start=zoom)
      folium.Marker(location=address).add_to(map)
      map.save('map.html')
      with open('map.html') as f:
          hti.screenshot(f.read(), save_as='map.jpg')
      await message.channel.send(file=discord.File(r'map.jpg'))
      os.remove('map.html')
      os.remove('map.jpg')
      return
    else:
      await message.channel.send('Invalid IP')
      return

client.run(TOKEN)

#the command is !locate [ip] [zoom=int]
