import asyncio
import discord
from settings import *
import random
import requests
import re
import json
import time
import os
import youtube_dl
from bs4 import BeautifulSoup
from discord import Game
from discord.ext.commands import Bot

client = Bot(command_prefix=BOT_PREFIX)

@client.event
async def on_ready():
    print("Logged in as " + client.user.name)

@client.command(aliases=["meme", "dank"])
async def dankmeme(ctx):
    redditHTML = requests.get("https://www.reddit.com/r/dankmemes/new/", headers=REQUESTSHEADER)
    reddit = BeautifulSoup(redditHTML.content, "html.parser")
    link = reddit.body.find("h3").parent.parent
    time.sleep(3)
    redditHTML = requests.get("https://www.reddit.com" + link.get("href"), headers=REQUESTSHEADER)
    reddit = BeautifulSoup(redditHTML.content, "html.parser")
    await ctx.channel.send(reddit.body.find("img", attrs={"alt": "Post image"}).get("src"))

@client.command(aliases=["user", "steam", "vac", "steamid", "steamprofile", "profile", "id"])
async def steamuser(ctx, username):
    try:
        cleaner = re.compile('<.*?>')
        rawsite = requests.get(f"https://steamidfinder.com/lookup/{username}")
        site = BeautifulSoup(rawsite.content, "html.parser")
        div = site.body.find("div", attrs={"class":"panel-body"})
        codes = div.find_all("code")

        rawsite = requests.get(f"http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key=CB0ECDFAA33531C92152452DEA3DA86A&steamids={codes[2]}")
        bans = json.loads(rawsite.content)

        await ctx.channel.send(ctx.author.mention + re.sub(cleaner, "", f'\n**Name:** `{codes[7]}`\n**Profile state:** `{codes[5]}`\n**CommunityBan:** `{bans["players"][0]["CommunityBanned"]}`\n**VACBans:** `{bans["players"][0]["NumberOfVACBans"]}`   Days since: `{bans["players"][0]["DaysSinceLastBan"]}`\n**GameBans:** `{bans["players"][0]["NumberOfGameBans"]}`\n**EconomyBans:** `{bans["players"][0]["EconomyBan"]}`\n**SteamID:** `{codes[2]}`\n**Profile:** {codes[4]}'))
    except:
        await ctx.channel.send("Wrong name!")

@client.command(aliases=["news", "new", "sn"])
async def steamnews(ctx, game):
    jsonRaw = requests.get(f"http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={gameIDs[game]}&count=3&maxlength=300&format=json")
    data = json.loads(jsonRaw.content)
    await ctx.channel.send(f'{ctx.author.mention}, {game} news for you!\n**{data["appnews"]["newsitems"][0]["title"]}***\n{data["appnews"]["newsitems"][0]["contents"]}\n__{data["appnews"]["newsitems"][0]["author"]}__ Link: <{data["appnews"]["newsitems"][0]["url"]}>')

@client.command(aliases=["csgo", "update", "updates", "csgoupdates"])
async def csgoupdate(ctx):
    htmlData = requests.get("https://blog.counter-strike.net/index.php/category/updates/")
    data = BeautifulSoup(htmlData.content, "html.parser")
    post = data.body.find("div", attrs={"class": "inner_post"} )
    cleaner = re.compile('<.*?>')
    await ctx.channel.send(f'{ctx.author.mention}, CSGO updates for you!\n{re.sub(cleaner, "", str(post.find_all("p")[1]))}')

@client.command(name="random", aliases=["rand", "randrange"])
async def rand(ctx, a, b):
    await ctx.channel.send(str(random.randrange(int(a), int(b))))

@client.command(aliases=["loop", "loopback", "mirror", "mimic"])
async def echo(ctx, msg):
    await ctx.channel.send(msg)

@client.command(aliases=["join", "j"])
async def join_voice(ctx):
    for vc in client.voice_clients:
        vc.disconnect()
    await ctx.author.voice.channel.connect()

@client.command(aliases=["leave", "dc"])
async def leave_voice(ctx):
    for vc in client.voice_clients:
        await vc.disconnect()

@client.command(aliases=["p", "yt", "youtube"])
async def play(ctx, songname):
    for fn in os.listdir("./"):
        if fn.endswith(".mp3"):
            os.remove(fn)

    with youtube_dl.YoutubeDL(YTDL_OPS) as ydl:
        ydl.download([f"ytsearch:{songname}"])

    for fn in os.listdir("./"):
        if fn.endswith(".mp3"):
            os.rename(fn, "song.mp3")

    for vc in client.voice_clients:
        vc.stop()

    if (len(client.voice_clients) == 0):
        await ctx.author.voice.channel.connect()

    try:
        client.voice_clients[0].play(discord.FFmpegPCMAudio("song.mp3"))
    except:
        await ctx.channel.send("Can't play!")
        print("Can't play!")

@client.command(aliases=["pp", "resume"])
async def pause(ctx):
    try:
        for vc in client.voice_clients:
            if vc.is_palying():
                vc.pause()
            elif vc.is_paused():
                vc.resume()
    except:
        print("Something went wrong while pausing/resuming!")

@client.command(aliases=["s"])
async def stop(ctx):
    for vc in client.voice_clients:
        vc.stop()

client.activity = Game(name=ACTIVITY)
client.run(TOKEN)