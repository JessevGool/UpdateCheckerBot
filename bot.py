import os
import json
import discord
from discord.ext import commands
client = commands.Bot(command_prefix= '|')


@client.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f"Cog: {extension} loaded")

@client.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f"Cog: {extension} unloaded")

@client.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f"Cog: {extension} reloaded")
    except:
            await ctx.send(f"Extension doesn't exist {ctx.message.author.nick}")



for filename in os.listdir('cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

with open('config/secrets.json') as secrets:
    secrets = json.load(secrets)

client.run(secrets['token'])