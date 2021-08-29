import discord 
from discord.ext import commands , tasks
import asyncio
import random
import datetime
from pymongo import MongoClient

from core import *

from dotenv import dotenv_values
VALUES = dotenv_values("paradox-bot/venv/.env")
cluster = MongoClient(VALUES["DB_URI"])


class giveaways(commands.Cog):
  """Giveaways"""
  def __init__(self, client):
    self.client = client


  @commands.command()
  async def gstart(self, ctx, time=None, *, prize:str=None):
    """Start a Quick Simple Giveaway"""

    da_prefix = await get_prefix(ctx.message)

    error_embed = discord.Embed(color = ctx.author.color)
    if not time:
      error_embed.add_field(name=":tada: Please include a length of time, number of winners and a prize" , value= f"Example usage : {da_prefix}gstart 30m Human Civilization")
      await ctx.send(embed = error_embed)
      return
    if not prize:
      error_embed.add_field(name=":tada: Please include the prize that you want to giveaway" , value= f"Example usage : {da_prefix}gstart 30m Human Civilization")
      await ctx.send(embed = error_embed)
      return

    time = convert_time(time)

    if time == -1:
      await ctx.send("You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
      return
    elif time == -2:
      await ctx.send("The time must be an integer please enter an integer next time")
      return
    t_delta = datetime.timedelta(seconds= time)
    t_now = datetime.datetime.utcnow()
    t_end = t_now + t_delta

    g_embed = discord.Embed(
      title = prize,
      description = f"React with :tada: to enter!\nEnds: <t:{int(t_end.timestamp())}:R> (<t:{int(t_end.timestamp())}:f>)\nHosted by : {ctx.author.mention}",
      color = ctx.author.color,
      timestamp = t_end,
      )
    g_embed.set_footer(text="Ends at ")

    my_msg = await ctx.send(":tada: **GIVEAWAY** :tada:", embed = g_embed)
    await my_msg.add_reaction("🎉")
    await ctx.message.delete()

    await asyncio.sleep(time)

    new_msg = await ctx.channel.fetch_message(my_msg.id)
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(self.client.user))
    if ctx.author in users:
      users.pop(users.index(ctx.author))

    winner = random.choice(users)

    await ctx.send(f"Congratulations {winner.mention} won the **{prize}** !")
    await new_msg.remove_reaction("🎉", winner)




  @commands.command()
  async def gcreate(self, ctx):
    "Interactive Giveaway Setup!"

    parameters = [
          "In which channel do you want to post the giveaway in?",
          "How many Number of Winners are there?"
          "What is the giveaway about?",
          "How long should the giveaway last? (type in  s | m | h | d ) ",
      ]

    parameters_ans = []

    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel

    def check_reaction(reaction, user):
      return reaction.message.id == msg.id and user == ctx.author and str(reaction.emoji) == "❌"


    for i in range(len(parameters)):
      check_loop = "0"
      while check_loop == "0":
        p_embed = discord.Embed(
          color = 0x00afff
        )
        p_embed.add_field(name= f"Giveaway Setup ({i}/{len(parameters)}" , value= parameters[i])
        p_embed.set_footer(text="CLick on the ❌ if you wish to cancel the process")
        msg = await ctx.channel.send(embed = p_embed)
        await msg.add_reaction(emoji= "❌")

        done, pending = await asyncio.wait([
          self.client.wait_for('message', check = check, timeout = 40.0),
          self.client.wait_for('reaction_add', check = check_reaction, timeout = 40.0)
        ], return_when= asyncio.FIRST_COMPLETED)

        try:
          stuff = done.pop().result()       
          
        except asyncio.TimeoutError:
          await ctx.send("You did not answer in time, please be quicker next time!")
          future.exception()
          check_loop == "1"
          return

        else:
            if isinstance(stuff, discord.message.Message):
              if i == 0 :
                if stuff is discord.TextChannel:
                  await ctx.send("Confirmed")
              elif i == 1:
                if stuff.content is int:
                  await ctx.send("int confirmed")
                pass
              elif i == 2:
                prize = str(stuff.content)
              elif i == 3:
                await ctx.send("u sent me time? huh mf ")
              check_loop = "1"

            elif isinstance(stuff, tuple):
              await ctx.send("Cancelled the giveaway!")
              return

            else:
              await ctx.send(f"Please Mention the Channel properly, like this {ctx.channel.mention}")

        for future in pending:
          future.cancel()


  @commands.command()
  async def greroll(self, ctx, msg_id:int):
    new_msg = await ctx.channel.fetch_message(msg_id)
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(self.client.user))
    if ctx.author in users:
      users.pop(users.index(ctx.author))

    winner = random.choice(users)

    await ctx.send(f"Congratulations {winner.mention} won the **Giveaway** !") #prize instead of giveaway , database
    await new_msg.remove_reaction("🎉", winner)


  @commands.command()
  async def gend(self, ctx, msg_id:int):
    new_msg = await ctx.channel.fetch_message(msg_id)
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(self.client.user))
    if ctx.author in users:
      users.pop(users.index(ctx.author))

    winner = random.choice(users)

    await ctx.send(f"Congratulations {winner.mention} won the **Giveaway** !") #prize instead of giveaway , Object oriented programming , database or somethign
    await new_msg.remove_reaction("🎉", winner)




#----------------------------------------------------------------------
def setup(client):
  client.add_cog(giveaways(client))




    # await fetch_message
#SUGGESTIONS OF IMAGE GIVEN BY SEEING TEH PRIZE AND GIVING SUGGESTIONS OF TEMPLAETS OF IMAGES THAT CAN LOOK GOOD WITH THE GIVEAWAY OPTIONAL
#REQUIRMENTS, GIVEAWAY MANAGER ROLE INVIETE RECORDS
#Customization
#Server boost by pass
#bypass for only a certain giveaway 
#list the giveaways
#diffrent bypass roles and customization
#black list and white list
#beautiful embed 
#images optionla or myabe default random images
#images api 
#random images for the embed (can be changed)
#reward of giveaway winner role
#maybe stor data of giveaway winners and list of giveaway done and by whom
#guild join requirments

#maybe emachine learning algo or ai in it >>>> Stats and N.E.A.T Math








#ongoing giveaways will be lost on bot restart 
#how can we fix such shit
#database or something if this needs to go public