import discord 
from discord.ext import commands, ipc
from pymongo import MongoClient


cluster = MongoClient("mongodb+srv://db:databaseuser@paradox.n7mew.mongodb.net/paradox?retryWrites=true&w=majority")


db = cluster["paradox"]
g_configs = db["guild_configs"]



class ipc_file(commands.Cog):
    """Change the Configuration of the bot"""
    def __init__(self, client):
        self.client = client



    @ipc.server.route()
    async def get_guild_count(self, data):
        return len(self.client.guilds)


    @ipc.server.route()
    async def get_guild_ids(self, data):
        final = []
        for guild in self.client.guilds:
            final.append(guild.id)
        return final




    @ipc.server.route()
    async def get_guild(self, data):
        guild = self.client.get_guild(data.guild_id)
        if guild is None: return None

        guild_data = {
            "name": guild.name,
            "id": guild.id,
            "prefix" : "?"
        }

        return guild_data





#----------------------------------------------------------------------
def setup(client):
  client.add_cog(ipc_file(client))
