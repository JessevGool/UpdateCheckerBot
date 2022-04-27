import discord
from discord.ext import commands, tasks
from itertools import cycle
import os

class Events(commands.Cog):
    status = cycle(["|help for help",""])

    async def printDEBUG(self,message):
        DEBUG_CHANNEL = self.client.get_channel(701548889118998598)
        await DEBUG_CHANNEL.send(message)

    
    def __init__(self,client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as: ',self.client.user)
        print("OS: " + os.name)
        self.change_status.start()

    @tasks.loop(seconds=60)
    async def change_status(self):
        await self.client.change_presence(activity=discord.Game(next(self.status)))

def setup(client):
    client.add_cog(Events(client))