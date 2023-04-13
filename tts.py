import discord
from discord.ext import commands
import asyncio
from gtts import gTTS
import tempfile
your_id = "your_id" # works for one person only to prevent spam extremely easy to change if you want for multiple people?
bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())
voice_client = None
@bot.event
async def on_message(message):
    global voice_client
    if message.author == bot.user:
        return
    if message.author.id == int(your_id):
     if message.author.voice and message.content:
         voice_channel = message.author.voice.channel
         if voice_client and voice_client.is_connected():
             if voice_client.channel != voice_channel:
                 await voice_client.move_to(voice_channel)
         else:
             voice_client = await voice_channel.connect()
         tts = gTTS(text=message.content, lang='en', tld='com.au')
         with tempfile.NamedTemporaryFile(delete=False) as fp:
             tts.write_to_fp(fp)
             fp.flush()
             fp.seek(0)
             voice_client.play(discord.FFmpegPCMAudio(fp.name))
             while voice_client.is_playing():
                 await asyncio.sleep(1)
             await asyncio.sleep(300)  
             if not any(voice_client.channel.members):
                 await voice_client.disconnect()
    elif voice_client and voice_client.is_connected() and not any(voice_client.channel.members):
        await voice_client.disconnect()
        voice_client = None

bot.run('Your token here')