import discord 
from discord.ext import commands

class plx(commands.Cog):
  """Have some fun Trying these commands"""
  def __init__(self, client):
    self.client = client

  @commands.commnad()
  async def fuckyou(self, ctx):
      await ctx.send("YEAH")



"""MAKE CHEKC THAT CHECK IS THE COMMAND IS CALLED FROM THE PLX GUILD THEN ONLY RUYN MAYBE WE CAN KEEP A PLACE HOLER OR SOMETHING"""






#----------------------------------------------------------------------
def setup(client):
  client.add_cog(plx(client))




