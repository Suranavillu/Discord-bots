import discord
from discord.ext import commands
import yt_dlp
import asyncio

TOKEN = "Enter your bot token here"

intents = discord.Intents.default()
intents.message_content = True

#You can change the bot name if you wish to, i set columbina for mine
columbina = commands.Bot(command_prefix = '!co', intents = intents)

#set options for ffmpeg, this includes option to reconnect and option for no video
ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

#just a custom activity, replace whatever you want in the name field and the bot will display it in profile
@columbina.event
async def on_ready():
    await columbina.change_presence(activity = discord.CustomActivity(name = "Watching over Sura"))
    print("Columbina is ready to stream music!")

#this is to prevent the bot from getting triggered from its own messages
@columbina.event
async def on_message(message):
    if message.author == columbina.user:
        return
    await columbina.process_commands(message)

#can change audio quality here 
ydl_opts = {
    'format' : 'bestaudio',
    'quiet' : True,
    'extractor_args': {'youtube': {'js_runtimes': ['nodejs']}}
}

queues = {}

#play next function
def play_next(ctx):
    guild_id = ctx.guild.id
    if guild_id not in queues or not queues[guild_id]:
        return
    song = queues[guild_id].pop(0)
    ctx.voice_client.play(discord.FFmpegPCMAudio(song['url'], **ffmpeg_opts), after = lambda e: play_next(ctx))
    #send embed for playing now
    embed = discord.Embed(title = f"Now playing:💽",
                          description = song['title'],
                          color = discord.Color.blue(),)
    embed.add_field(name = f"Requested by: ", value = ctx.author.mention)
    asyncio.run_coroutine_threadsafe(ctx.send(embed = embed), ctx.bot.loop)


#to join the vc
@columbina.command()
async def play(ctx, *, query):
    if not ctx.author.voice:
        await ctx.channel.send(f"Hey {ctx.author.mention} you have to be in a vc to stream music!")
    else:
        if ctx.voice_client:
            vc_to_join = ctx.voice_client
        else:
            vc_to_join = await ctx.author.voice.channel.connect()
        await ctx.reply("Preparing or adding it to queue to stream music...🎶")

        #audio fetching
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download = False)
            url = info['entries'][0]['url']
        
        #put obtained song to queue
        guild_id = ctx.guild.id
        if guild_id not in queues:
            queues[guild_id] = []
        queues[guild_id].append({'url': url, 'title': info['entries'][0]['title'], 'requester': ctx.author.mention})

        #successful queue addition display
        if ctx.voice_client.is_playing():
            await ctx.reply(f"Your song has been added to queue")
        else:
            play_next(ctx)

#to leave vc
@columbina.command()
async def leave(ctx):
    vc_to_leave = ctx.voice_client

    if not ctx.author.voice:
        await ctx.reply("You need to be in a VC~")
    elif not ctx.voice_client:
        await ctx.reply("I'm not in a VC!")
    elif ctx.author.voice.channel != ctx.voice_client.channel:
        await ctx.reply("Hey it's rude to ruin others fun without being in a vc! (And don't join and ruin it too...)")
    else:
        await ctx.voice_client.disconnect()

#vc music skip/stop 
@columbina.command()
async def skip(ctx):
    music_to_stop = ctx.voice_client

    if not ctx.author.voice:
        await ctx.reply("You need to be in a VC~")
    elif ctx.author.voice.channel != ctx.voice_client.channel:
        await ctx.reply("Hey it's rude to ruin others fun without being in a vc! (And don't join and ruin it too...)")
    elif not ctx.voice_client:
        await ctx.reply("I'm not in a VC!")
    else:
        ctx.voice_client.stop()
        await ctx.reply(f"{ctx.author.mention} has requested me to Skip/Stop~\nIf there songs in queue it will be played automatically!")

#check queue
@columbina.command()
async def queue(ctx):
    queue = ctx.guild.id
    if queue not in queues or not queues[queue]:
        await ctx.reply("The queue is empty~ add some songs to fill it!")
    else:
        queue_list = ""
        embed = discord.Embed(title = "Current Queue 🎵", color = discord.Color.dark_gold())
        for i, song in enumerate(queues[queue], start = 1):
            queue_list += f"`{i}.` {song['title']} Requested by {song['requester']}\n"
            embed.description = queue_list 
        await ctx.send(embed = embed)

#list the bot commands
@columbina.command()
async def clscmd(ctx):
    await ctx.send(f"Hey {ctx.author.mention} here are my commands:\n[1] `!coplay 'your song name or link'` plays or adds your song to the queue\n[2]`!coqueue` to display what songs are in the queue\n[3]`!coleave` to make me leave the VC\n[4]`!coskip` to skip song that's currently playing")


columbina.run(TOKEN)