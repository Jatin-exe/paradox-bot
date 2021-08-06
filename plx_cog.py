import discord 
from discord.ext import commands

class plx(commands.Cog):
  """Have some fun Trying these commands"""
  def __init__(self, client):
    self.client = client

  @commands.commnad()
  async def fuckyou(self, ctx):
      await ctx.send("YEAH")










#----------------------------------------------------------------------
def setup(client):
  client.add_cog(plx(client))




