import discord 
from discord.ext import commands , tasks
import os
import sys
import json
import asyncio


channels = ["Bot Channel", "Suggestion Channel", "Starboard Channel", "Mute Channel", "Gulag Channel", "Announcements Channel"]
roles = ["Mod Role", "Admin Role", "Muted Role"]



class tasks(commands.Cog):
  """Background Tasks"""
  def __init__(self, client):
    self.client = client

  @tasks.loop()
  async def mute_check(self):
    with open("Jsons\\basic.json", "r")as f:
      basic = json.load(f)
    
    #if baisc[str(guild.id)]:
      #print(basic[str(guild.id)])

  @commands.listener()
  async def on_guild_channel_create(self, channel):
    pass


      


























#----------------------------------------------------------------------
def setup(client):
  client.add_cog(tasks(client))
