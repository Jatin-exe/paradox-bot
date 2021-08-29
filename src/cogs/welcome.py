import discord
from discord.ext import commands
from pymongo import MongoClient


from dotenv import dotenv_values
VALUES = dotenv_values("paradox-bot/venv/.env")
cluster = MongoClient(VALUES["DB_URI"])

db = cluster["paradox"]
w_data = db["welcome_data"]

#help commadn for setting up level
#welcome msg not being stored
class welcome(commands.Cog):
  """Welcome!"""
  def __init__(self, client):
    self.client = client

#WELCOME --------------------------------------bb

  @commands.Cog.listener()
  async def on_member_join(self, member):
    w_dict = w_data.find_one({"_id": member.guild.id})
    if w_dict is not None:
      w_ch = w_dict["welcome_channel"]
      w_msg = w_dict["welcome_msg"]

      w_ch = self.client.get_channel(int(w_ch))
      #await w_ch.send(f"{w_msg}") #incluedde varial, templates , embeds , maybe store templates on user acc
      #Welcome msg custom not the one i am using lol
    
      await w_ch.send(f'**{w_msg} Welcome {member.mention} to {member.guild.name}!! {w_msg}**')

  
  @commands.command(aliases = ["setupwelcome", "setwelcome"])
  @commands.has_permissions(manage_guild=True)
  async def welcomesetup(self,ctx, welcome_channel:discord.TextChannel= None,*, welcome_msg:str=None):
    if welcome_channel is None:
      await ctx.send('You did not define your Welcome Channel!')
      return
    if welcome_msg is None:
      await ctx.send('You did not define your Welcome Message')
      return
    
    welcome_channel_id = welcome_channel.id

    w_obj = {
      "_id": ctx.guild.id,
      "welcome_channel": welcome_channel_id,
      "welcome_msg": welcome_msg
      }

    w_data.replace_one({"_id": ctx.guild.id}, w_obj, True)
    
    await ctx.send(f'Setup Done!\nWelcome Channel: {welcome_channel.mention}\nWelcome Message: {welcome_msg}') 



  @commands.command()
  async def welcometest(self, ctx):
    w_dict = w_data.find_one({"_id": ctx.guild.id})
    if w_dict is None:
      await ctx.send("You didn't define your welcome channel and message!, you can do so by using ```.welcomesetup```")

    w_msg = w_dict['welcome_msg']
    w_ch = w_dict["welcome_channel"]

    w_ch = self.client.get_channel(int(w_ch))

    await w_ch.send(w_msg)










#----------------------------------------------------------------------------------------------------------------------------
def setup(client):
  client.add_cog(welcome(client))





#RANDOOM MESSAGES FUN AND CREATIVE IN STEAD OF CONSTANT SAME MESSAGES 
#ASK FOR SUGGGESTIONS ON WELCOME MESSAGE
