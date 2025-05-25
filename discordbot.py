
# import discord
# import requests
# import json

# def get_meme():
#   response = requests.get('https://meme-api.com/gimme')
#   json_data = json.loads(response.text)
#   return json_data['url']

# class MyClient(discord.Client):
#   async def on_ready(self):
#     print('Logged on as {0}!'.format(self.user))
#   async def on_message(self, message):
#     if message.author == self.user:
#         return
#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello World!')
#     if message.content.startswith('$meme'):
#       await message.channel.send(get_meme())

# intents = discord.Intents.default()
# intents.message_content = True

# client = MyClient(intents=intents)
# client.run('') # Replace with your bot token


import discord
from discord.ext import commands
import yt_dlp

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"🔊 Joined {channel.name}")
    else:
        await ctx.send("❌ You're not in a voice channel.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 Left the voice channel.")
    else:
        await ctx.send("❌ I'm not connected to any voice channel.")

@bot.command()
async def play(ctx, *, url):
    voice_client = ctx.voice_client
    if not voice_client:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
            voice_client = ctx.voice_client
        else:
            return await ctx.send("❌ You need to be in a voice channel.")

    ydl_opts = {
        'format': 'bestaudio',
        'quiet': False,
        'default_search': 'auto',
        'noplaylist': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']
        title = info.get('title')

    source = discord.FFmpegPCMAudio(audio_url, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5')
    if voice_client.is_playing():
        voice_client.stop()

    voice_client.play(source, after=lambda e: print("Playback finished."))
    await ctx.send(f"▶️ Now playing: **{title}**")

bot.run("") # Replace with your bot token
