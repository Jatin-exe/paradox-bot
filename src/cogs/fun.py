import discord 
from discord.ext import commands
import random
from pymongo import MongoClient
import asyncio
import datetime


from dotenv import dotenv_values
VALUES = dotenv_values("paradox-bot/venv/.env")
cluster = MongoClient(VALUES["DB_URI"])

from core import *

#obj orienttednt sel.attributes


class fun(commands.Cog):
  """Have some fun Trying these commands"""
  def __init__(self, client):
    self.client = client


  
#AFK-------------------------------------------------------------


  @commands.Cog.listener()
  @commands.check(no_dm)
  async def on_message(self, message):
    db = cluster["paradox"]
    afk = db["afk"]

    #PREVENT SELF PINGING AND FLOODING , PREVENT MORE THAN ONE MENTION PING AND FLOODING #ASAP BRO
    if not message.author.bot:
      if hasattr(message, "mentions"):
        if len(message.mentions) == 1:
          for x in message.mentions:
            if not x.bot:
              afk_data = afk.find_one({"_id": x.id})
              if afk_data is not None:            
                if afk_data["afk"] == True:
                  afk_reason = afk_data["afk_reason"]
                  embed = discord.Embed(color = 0x00afff)
                  embed.add_field(name= f"{x.name} is currently AFK!", value= f"Reason: {afk_reason}")
                  embed.set_footer(text= f"Mentioned by {message.author.name}")
                  await message.channel.send(embed = embed, delete_after= 7)

    g_prefix = await get_prefix(message)

    if message.content.startswith("."):
      return

    elif message.content.startswith(str(g_prefix)):
      return
    afk_data = afk.find_one({"_id": message.author.id})

    if afk_data is None:
      return
    if afk_data["afk"] is False:
      return
    
    if afk_data["afk"] is True:
      afk.update_one({"_id": message.author.id}, {"$set": {"afk_reason": None, "afk": False}})
      await message.channel.send(f'{message.author.mention} is no longer AFK!', delete_after= 4)
      try:
        await message.author.edit(nick=f'{message.author.display_name[6:]}')
      except:
        return

  @commands.command(aliases= ["AFK", "Afk"])
  async def afk(self, ctx, *, afk_reason="None"):
    """Show that you are Afk!"""
    db = cluster["paradox"]
    afk = db["afk"]
    afk_obj = {
      "_id": ctx.author.id,
      "guild_id": ctx.guild.id,
      "afk": True,
      "afk_reason": afk_reason
      }
    
    if afk.find_one({"_id": ctx.author.id}) is None:
      afk.insert_one(afk_obj)
    else:
      afk.update_one({"_id": ctx.author.id}, {"$set" :{"afk": True, "afk_reason": afk_reason}})   
    await ctx.send(f'I set your **AFK** as {afk_reason}')
    try:
      await ctx.author.edit(nick=f'[AFK] { ctx.author.display_name}')
    except:
      return

  

#OTHER-----------------------------------------------------

  @commands.command()
  async def ping(self, ctx):
    """See the Ping of dis Bot"""
    #BETTER PING - API PING , DATA BASE PING , SERVER PING AND A BIT MORE INFO , AVERAGE PING
    await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms')


  @commands.command()
  async def say(self, ctx, *, say):
    """Say anything you would like to say"""
    await ctx.send(f'{say}\n~{ctx.author}')
    await ctx.message.delete()

  @commands.command(Aliases= ["an_say", "Ansay"])
  async def ansay(self,ctx, *, say):
    """Say something while being Anonymous, No Judgment"""
    #NICE RANDOM FUNNY NAMES INSTEAD OF JUST ANONYMOUS
    emd = discord.Embed(
      description = say,
      color = 0x0000ff
    )
    emd.set_author(name="Anonymous")

    await ctx.send(embed=emd)
    await ctx.message.delete(delay=1)
    
    

  
  @commands.command(aliases= ["F"])
  async def f(self, ctx, *, reason=None):
    """Show some respect with this command"""
    if not reason:
      fembed = discord.Embed(
        title = f'**{ctx.author.display_name}** has paid their Respects!',
        colour = discord.Colour.from_rgb(1, 1, 1)
        )
      await ctx.send(embed=fembed)  

    else:
      fembed = discord.Embed(
        title = f'**{ctx.author.display_name}** has paid their Respects!',
        description = reason,
        colour = discord.Colour.from_rgb(1, 1, 1))

      await ctx.send(embed=fembed)

  @commands.command()
  @commands.has_permissions(mention_everyone= True)
  async def someone(self, ctx):
    "Mention a Random Person"
    check = True
    while check == True:
      someone = random.choice(ctx.guild.members)
      if someone.bot:
        check = True
      else:
        check = False
        await ctx.send(someone.mention)
      

  @commands.command()
  async def dnd(self, ctx, *, dnd_reason=None):
    """Show that you are Afk!"""
    #NO PING, GOOD FOR NO PINGS AND THINGS
    #PING == BAN!

    dnd_list = [
      "Living Life",
      "Touching Grass",
      "Ping == Block!"
    ]

    db = cluster["paradox"]
    dnd = db["dnd"]

    dnd_data = dnd.find_one({"_id": ctx.author.id})
    #if dnd_data:
      
    try:
      if dnd_reason is None:
        dnd_reason = random.choice(dnd_list)
        await ctx.author.edit(nick=f'{ ctx.author.display_name} (DND, {dnd_reason})')
        
      else:
        await ctx.author.edit(nick=f'{ ctx.author.display_name} (DND, {dnd_reason})')
    except:
      pass
    dnd_obj = {
      "_id": ctx.author.id, 
      "dnd": True,
      "dnd_reason": dnd_reason
      }

    dnd.insert_one(dnd_obj)
    await ctx.send(f'You wont be disturbed now <3', delete_after = 4)

    

  







#----------------------------------------------------------------------
def setup(client):
  client.add_cog(fun(client))

#IDEAS THOUGHTS

#PIN COMMANDS LIKE STAR BOARD BASED ON REACTION AND CAN BE DISABLED AND REACTION EMOJI CAN ALSO BE CHANGED AND NO OF REACTION CAN BE CHANGED AND MAYBE LOG OF WHO FIRST REACTED AND LOGGING CHANNEL SHOLD OR SHOULD NOT

#ROCK PAPER SCISSORS 
