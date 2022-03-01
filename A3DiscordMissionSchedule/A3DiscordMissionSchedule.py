from http import server
import discord
from discord.ext import commands

bot = discord.Bot()
servers = [945803024897564723]

@bot.slash_command(guild_ids = servers, name="test", description = "Testing things out")
async def test(ctx):
  print("Command recieved")
  await ctx.respond(f"I am working \n\nLatency: {bot.latency*1000} ms.")

@bot.event
async def on_message(message):
  print(f"Message from {message.author}: {message.content}")

bot.run('NDg0NDc3MTc3MzEyODM3NjMy.W4cSiA.bsURvBHLf6RaV2y8F55n_Huq9nU')
