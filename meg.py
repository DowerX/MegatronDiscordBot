import asyncio
import discord
from discord import Game
from discord.ext.commands import Bot
from settings import *
from pollsaddon import *
from random import randrange
from requests import get
from re import compile, sub
from json import loads
from time import sleep
from os import listdir, rename, remove
from youtube_dl import YoutubeDL
from bs4 import BeautifulSoup
import logging

logging.basicConfig(filename="bot_info.log", filemode="w",  format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

client = Bot(command_prefix=BOT_PREFIX)
client.activity = Game(name=ACTIVITY)

def rolecheck(usr, rqrl):
    rls = []
    for rl in usr.roles:
        rls.append(rl.name)
    return rqrl in rls

@client.command(aliases=["vote"])
async def poll(ctx, cmd, arga=None, argb=None):
    try:
        if cmd == "addpoll":
            addpoll(arga)
        elif cmd == "addtopoll":
            addtopoll(int(arga), argb)
        elif cmd == "vote":
            vote(int(arga), ctx.author.id, int(argb))
        elif cmd == "removepoll":
            removepoll(int(arga))
        elif cmd == "removefrompoll":
            removefrompoll(int(arga), int(argb))
        elif cmd == "getpolls":
            await ctx.channel.send("Polls:\n" + displaypolls())
        elif cmd == "getpoll":
            await ctx.channel.send("Poll:\n" + displaypoll(int(arga)))
        elif cmd == "results":
            await ctx.channel.send("Results:\n" + getvotes(int(arga)))
        elif cmd == "demo":
            demo()
    except:
        logging.error(f"polls failed thanks to {ctx.author}")


@client.event
async def on_ready():
    logging.info("Logged in as " + client.user.name)

@client.command(aliases=["meme", "dank"])
async def dankmeme(ctx):
    logging.info(f"{ctx.author.name} requested a dankmeme!")
    redditHTML = get("https://www.reddit.com/r/dankmemes/new/", headers=REQUESTSHEADER)
    reddit = BeautifulSoup(redditHTML.content, "html.parser")
    link = reddit.body.find("h3").parent.parent
    sleep(3)
    redditHTML = get("https://www.reddit.com" + link.get("href"), headers=REQUESTSHEADER)
    reddit = BeautifulSoup(redditHTML.content, "html.parser")
    await ctx.channel.send(reddit.body.find("img", attrs={"alt": "Post image"}).get("src"))

@client.command(aliases=["user", "steam", "vac", "steamid", "steamprofile", "profile", "id"])
async def steamuser(ctx, username):
    logging.info(f"{ctx.author.name} requested the SteamProfile info of {username}!")
    try:
        cleaner = compile('<.*?>')
        rawsite = get(f"https://steamidfinder.com/lookup/{username}")
        site = BeautifulSoup(rawsite.content, "html.parser")
        div = site.body.find("div", attrs={"class":"panel-body"})
        codes = div.find_all("code")

        rawsite = get(f"http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key=CB0ECDFAA33531C92152452DEA3DA86A&steamids={codes[2]}")
        bans = loads(rawsite.content)

        await ctx.channel.send(ctx.author.mention + sub(cleaner, "", f'\n**Name:** `{codes[7]}`\n**Profile state:** `{codes[5]}`\n**CommunityBan:** `{bans["players"][0]["CommunityBanned"]}`\n**VACBans:** `{bans["players"][0]["NumberOfVACBans"]}`   Days since: `{bans["players"][0]["DaysSinceLastBan"]}`\n**GameBans:** `{bans["players"][0]["NumberOfGameBans"]}`\n**EconomyBans:** `{bans["players"][0]["EconomyBan"]}`\n**SteamID:** `{codes[2]}`\n**Profile:** {codes[4]}'))
    except:
        await ctx.channel.send("Wrong name!")

@client.command(aliases=["news", "new", "sn"])
async def steamnews(ctx, game):
    logging.info(f"{ctx.author.name} requested the news for {game}!")
    jsonRaw = get(f"http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={gameIDs[game]}&count=3&maxlength=300&format=json")
    data = loads(jsonRaw.content)
    await ctx.channel.send(f'{ctx.author.mention}, {game} news for you!\n**{data["appnews"]["newsitems"][0]["title"]}***\n{data["appnews"]["newsitems"][0]["contents"]}\n__{data["appnews"]["newsitems"][0]["author"]}__ Link: <{data["appnews"]["newsitems"][0]["url"]}>')

@client.command(aliases=["csgo", "update", "updates", "csgoupdates"])
async def csgoupdate(ctx):
    logging.info(f"{ctx.author.name} requested the CSGO updates!")
    htmlData = get("https://blog.counter-strike.net/index.php/category/updates/")
    data = BeautifulSoup(htmlData.content, "html.parser")
    post = data.body.find("div", attrs={"class": "inner_post"} )
    cleaner = compile('<.*?>')
    await ctx.channel.send(f'{ctx.author.mention}, CSGO updates for you!\n{sub(cleaner, "", str(post.find_all("p")[1]))}')

@client.command(name="random", aliases=["rand", "randrange"])
async def rand(ctx, a, b):
    logging.info(f"{ctx.author.name} requested a random number, {a}-{b}!")
    await ctx.channel.send(str(randrange(int(a), int(b))))

@client.command(aliases=["loop", "loopback", "mirror", "mimic"])
async def echo(ctx, msg):
    logging.info(f"{ctx.author.name} requested to echo the following: {msg}!")
    await ctx.channel.send(msg)

@client.command(aliases=["join", "j"])
async def join_voice(ctx):
    if not rolecheck(ctx.author, "DJ"):
        return

    logging.info(f"{ctx.author.name} requested me to join his voice channel!")
    for vc in client.voice_clients:
        vc.disconnect()
    await ctx.author.voice.channel.connect()

@client.command(aliases=["leave", "dc"])
async def leave_voice(ctx):
    if not rolecheck(ctx.author, "DJ"):
        return

    logging.info(f"{ctx.author.name} requested me to leave the current voice channel!")
    for vc in client.voice_clients:
        await vc.disconnect()

@client.command(aliases=["p", "yt", "youtube"])
async def play(ctx, songname):
    if not rolecheck(ctx.author, "DJ"):
        return

    logging.info(f"{ctx.author.name} requested me to play {songname} in his current voice channel!")
    for fn in listdir("./"):
        if fn.endswith(".mp3"):
            remove(fn)

    with YoutubeDL(YTDL_OPS) as ydl:
        ydl.download([f"ytsearch:{songname}"])

    for fn in listdir("./"):
        if fn.endswith(".mp3"):
            rename(fn, "song.mp3")

    for vc in client.voice_clients:
        vc.stop()

    if (len(client.voice_clients) == 0):
        await ctx.author.voice.channel.connect()

    try:
        client.voice_clients[0].play(discord.FFmpegPCMAudio("song.mp3"))
    except:
        await ctx.channel.send("Can't play!")
        logging.info("Can't play!")

@client.command(aliases=["pp", "resume"])
async def pause(ctx):
    if not rolecheck(ctx.author, "DJ"):
        return

    logging.info(f"{ctx.author.name} requested me to pause/resume the music!")
    try:
        for vc in client.voice_clients:
            if vc.is_palying():
                vc.pause()
            elif vc.is_paused():
                vc.resume()
    except:
        logging.info("Something went wrong while pausing/resuming!")

@client.command(aliases=["s"])
async def stop(ctx):
    if not rolecheck(ctx.author, "DJ"):
        return

    logging.info(f"{ctx.author.name} requested me to stop the music!")
    for vc in client.voice_clients:
        vc.stop()

client.run(TOKEN)