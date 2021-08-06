import discord 
from discord.ext import commands
import os
import sys
import json
from asyncio import sleep
import asyncio 
import datetime


class suggestions(commands.Cog):
  """Suggestions"""
  def __init__(self, client):
    self.client = client


#SUGGESTION 
  @commands.command()
  async def suggest(self, ctx, *,suggestion):
    with open(r'/home/ubuntu/Jsons/basic.json', 'r')as f:
      basic = json.load(f)
      bot_channel = basic[f'{ctx.guild.id}']['Bot Channel']
      bot_channel = self.client.get_channel(int(bot_channel))

      suggestion_channel = basic[f'{ctx.guild.id}']['Suggestion Channel']

    if suggestion_channel is None:
      await bot_channel.send(f"{ctx.author.mention} the suggestion channle is not set, notify the staff of the server about it!")

    else:
      if not suggestion:
        await bot_channel.send(f"{ctx.author.mention} your suggestion is sent in {bot_channel.mention}")
        await ctx.send(bot_channel)
      else:

        suggestion_channel = self.client.get_channel(int(suggestion_channel))
        
        s_embed = discord.Embed(color = 0x0000ff)

        s_embed.add_field(name= f"{ctx.author.name}'s Suggestion", value= suggestion)
        
        suggestion_embed = await suggestion_channel.send(embed = s_embed)

        await suggestion_embed.add_reaction(emoji= "⬆️")
        await suggestion_embed.add_reaction(emoji= "⬇️")

        await ctx.message.delete(delay=5)






#--------------------------------------------------------------------------
def setup(client):
  client.add_cog(suggestions(client))
