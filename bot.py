import random
import discord
from discord.ext import commands
from darksky.api import DarkSkyAsync
from darksky.types import languages, units
import aiohttp
import geocoder
import sys
import pyjokes
import lyricsgenius
import os

genius = lyricsgenius.Genius(os.environ["GENIUS_API"])
darksky = DarkSkyAsync(os.environ["DARKSKY_API"])
bot = commands.Bot(command_prefix=">")

@bot.command(description="Wyświetl temperature w podanej lokacji")
async def weather(ctx, *location: str):
    location = " ".join(location)
    g = geocoder.osm(location)
    forecast = await darksky.get_forecast(
        g.osm["y"],
        g.osm["x"],
        values_units=units.UK2,
        client_session=aiohttp.ClientSession(),
        lang=languages.POLISH,
    )
    w = forecast.currently
    print(w.icon)
    await ctx.send(f"Temperatura w {location} wynosi: {w.temperature}℃")
    await ctx.message.add_reaction("🌎")

@bot.command(description="Wylosuj losową liczbę z zakresu 1-6")
async def roll(ctx):
    result = str(random.randint(1, 6))
    await ctx.send(f"Wylosowałem {result}")
    await ctx.message.add_reaction("🤔")

@bot.command(description="Opowiedz losowy żart")
async def joke(ctx):
    joke = pyjokes.get_joke()
    await ctx.send(f"Uwaga dowcip: {joke}")
    await ctx.message.add_reaction("😂")

@bot.command(description="Wylosuj jeden z podanych wyborów")
async def choose(ctx, *choices: str):
    choice = random.choice(choices)
    await ctx.send(f"Wybieram {choice}!")
    await ctx.message.add_reaction("🙄")

@bot.command(description="Ocenię podaną rzecz w skali 1-10")
async def rate(ctx, *thing: str):
    thing = " ".join(thing)
    result = str(random.randint(1, 10))
    await ctx.send(f"Oceniam {thing} na {result}!")
    await ctx.message.add_reaction("💩")

@bot.command(name="is", description="Zdecyduj, czy podane stwierdzenie jest prawdziwe")
async def is_(ctx, *thing: str):
    thing = " ".join(thing)
    if random.choice([True, False]):
        await ctx.send(f"Tak, '{thing}' jest prawdą.")
        await ctx.message.add_reaction("✔")
    else:
        await ctx.send(f"Nie, '{thing}'' nie jest prawdą")
        await ctx.message.add_reaction("❌")

@bot.command(description="Znajdź tekst piosenki")
async def lyrics(ctx, *song_name):
    song_name = " ".join(song_name)
    song = genius.search_song(song_name)
    if song:
        lyrics = song.lyrics.strip().split("\n\n")
        await ctx.message.add_reaction("🎶")
        for paragraph in lyrics:
            await ctx.send(paragraph)
    else:
        await ctx.send(f"Nie mogłem znaleźć tekstu do piosenki {song_name}!")
        await ctx.message.add_reaction("😭")

bot.run(os.environ["DISCORD_API"])
