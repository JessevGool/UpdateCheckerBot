
from Objects.UpdateChecker import UpdateChecker
import time
from discord.ext import commands, tasks


updateClient = ""
class UpdateMessenger(commands.Cog):
    @tasks.loop(minutes=10)
    async def check_for_update(self):
        print("Checking for updates...")
        await self.checker.checkforModpackUpdates()
        print("Checking for updates...Done")
        print("Last check at: " + time.strftime("%H:%M:%S"))
    @commands.Cog.listener()
    async def on_ready(self):
        self.checker = UpdateChecker(updateClient)
        await self.checker.compareDBModsToPresetMods()
        self.check_for_update.start()
def setup(client):
    client.add_cog(UpdateMessenger(client))
    global updateClient
    updateClient = client