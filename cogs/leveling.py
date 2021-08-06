import discord 
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from pymongo import MongoClient
import asyncio
import typing

cluster = MongoClient("mongodb+srv://db:databaseuser@paradox.n7mew.mongodb.net/paradox?retryWrites=true&w=majority")





class levels(commands.Cog):
  """check your Level"""
  def __init__(self, client):
    self.client = client
    self._cd = commands.CooldownMapping.from_cooldown(1, 60, commands.BucketType.user) # Change accordingly
    



#Custom help commands
  @commands.command(aliases=["levelsetup", "setupleveling"])
  @commands.cooldown(2, 200, BucketType.user)
  @commands.cooldown(2, 200, BucketType.guild)
  async def levelingsetup(self, ctx):
    """Setup Leveling System, (interactive setup)"""
    leveling_parameters = [
      "**Which channels should not gain xp?** ( Mention all of them in a single message)",
      "**At which Levels do you want the roles to be given?** (Seperate the levels with a comma!, Example: `10, 20, 30, 40, 50`)",
      "**The Bot will make roles for the levels you mentioned and set it up! after the process is done you can change the names of the roles as you want | Send any txt to continue**",
      "**What should be the XP rate?** (Write it in multiplication format with `x` at the end, Example: `1.1x` or `2x` or `1.5x`)"
    ]


    ans_leveling_parameters = [] 

    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel

    def xp_check(msg):
      unit = msg[-1].lower()

      if unit != "x":
        return -1

      try:
        msg = float(msg[:-1])
        if msg < 1:
          return -3
        else:
          return msg
      except:
        return -2
 
      
    for i in range(len(leveling_parameters)):
      await ctx.send(leveling_parameters[i])

      try:
        msg = await self.client.wait_for('message',  timeout=100.0, check= check)
      except asyncio.TimeoutError:
        await ctx.send("You did not answer in time, please be quicker next time!")
        return
      else:
        if i == 0:
          if len(msg.channel_mentions) is 0:
            ans_leveling_parameters.append("None")
          else:
            ans_leveling_parameters.append(msg.channel_mentions)


        elif i == 1:
          ans_leveling_parameters.append(msg.content.split(","))



        elif i == 3:
          check_result = xp_check(msg.content)
          if check_result == -1:
            await ctx.send("Xp rate should end with a `x`, please try again")
            return
          elif check_result == -2:
            await ctx.send("Xp rate should be an integer, please try again")
            return
          elif check_result == -3:
            await ctx.send("Xp rate should not be less than 1, please try again")
            return
          elif check_result is float and check_result >= 1:
            ans_leveling_parameters.append(check_result[:-1])

    #END OF FOR LOOP
    try:
      no_xp_channels = []
      for ch in ans_leveling_parameters[0]:
        if isinstance(ch, "discord.TextChannel"): 
          no_xp_channels.append(ch)
          
    except:
      ctx.send(f"You did not mention the channel appropriately mention it like this {ctx.channel.mention} next time**" )
      return
    else:
      await ctx.send("Channel was mentioned successfuly")

    level_roles_at = ans_leveling_parameters[1]
    xp_rate = ans_leveling_parameters[3]

#CREATE ROLE WIHT NAEM AND PRMOT THAT U CAN COHANGE AND STORE THE ID OF THE ROLE THAT WAS STORED
    level_roles_id = []
    if len(level_roles_at) > 60:
      await ctx.send("Sorry u cant set more than 20 roles for Leveling System")
      return





    for i in level_roles_at:
      try:
        await ctx.send(type(level_roles_at))
        await ctx.send(level_roles_at)
        await ctx.send(i)
        float(i)
        if i > 100 or i < 0:
          await ctx.send("level should be between 1 and 100")
          return
        c_role = await ctx.guild.create_role(name= f"Level {i}", reason = "Level Role")
        level_roles_id.append(c_role.id)
      except:
        await ctx.send("invalid level was set")
        return
    db = cluster["paradox"]
    g_configs = db["guild_configs"]
    old_configs = g_configs.find_one({"_id": ctx.guild.id})
    if old_configs is None:
      old_configs = {
        "_id": ctx.guild.id,
        "prefix": ".",
        "roles": {},
        "channels": {"no_xp_channels": no_xp_channels},
        "leveling": {"level_roles_at": level_roles_at,"xp_rate": xp_rate, "level_roles_id": level_roles_id},
        "moderation": {},
      }
      g_configs.insert_one(old_configs)
    
    else:
      old_configs["leveling"] = {
        "level_roles_at": level_roles_at,
        "xp_rate": xp_rate,
        }
      old_configs["channels"]["no_xp_channels"] = no_xp_channels

      g_configs.replace_one({"_id": ctx.guild.id}, old_configs)

    await ctx.send("Leveling setup, you can always change these configs by doing this again, use ```.config leveling``` to see more info")







                                                        # rate, per, BucketType


#------------------  
  @commands.Cog.listener()
  @commands.cooldown(1, 60, BucketType.user)
  async def on_message(self, message):
    leveling_enable = True
    #ENABLE LEVELIGN

    def get_ratelimit(self, message: discord.Message) -> typing.Optional[int]:
        """Returns the ratelimit left"""
        bucket = self._cd.get_bucket(message)
        return bucket.update_rate_limit()

    if message.author.bot is True:
      return
    else:
      ratelimit = get_ratelimit(self, message)
      if ratelimit is None:
        if hasattr(message.author, 'guild'):
          db = cluster["paradox"]
          g_data = db["guild_configs"]
          g_configs = g_data.find_one({"_id": message.guild.id})
          if g_configs is not None:                                                     #["𒁷╎Level 10+", "𒁷╎Level 20+", "𒁷╎Level 30+", "𒁷╎Level 40+", "𒁷╎Level 50+"]
            level_roles = g_configs["leveling"]["level_roles_id"]
            level_num = g_configs["leveling"]["level_roles_at"]                           #[10,20,30,40,50]
            xp_rate = float(g_configs["leveling"]["xp_rate"])
            no_xp_channels = g_configs["channels"]["no_xp_channels"]
          
          else:
            return
        else:
          return
      else:
        return

        


    level_roles = [] #get roles from id and get obj

#-------------------------------------------

    db = cluster["leveling_guilds"]
    leveling = db[str(message.guild.id)]

    if str(message.channel.id) not in no_xp_channels:
      if not message.author.bot:
        stats = leveling.find_one({"_id" : message.author.id})
        if stats is None:
          newuser = {"_id" : message.author.id, "xp" : 100}
          leveling.insert_one(newuser)
        else:
          xp = stats["xp"] + 25*xp_rate
          leveling.update_one({"_id" : message.author.id}, {"$set":{"xp": int(xp)}})
          lvl = 0
          while True: #xp = 50
            if xp <= (50*(lvl**2))+(50*(lvl-1)):
               
              break
            lvl += 1
          xp -= (50*(lvl**2))+(50*(lvl-1))

#---------------------------------------

          if xp == 0:
            lvl += 1
            for i in range(len(level_roles)):
              if lvl == level_num[i]:
                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=level_roles[i]))
                embed = discord.Embed(description=f"{message.author.mention} you have gotten role **{level_roles[i]}!**")
                embed.set_thumbnail(url=message.author.avatar_url)
                await message.channel.send(embed=embed)
              else: 
                break 
          xp +=  (50*((lvl-1)**2))+(50*(lvl-1))
          




  @commands.command(aliases=["level", "stats", "xp"])
  async def rank(self, ctx):


    db = cluster["leveling_guilds"]
    leveling = db[str(ctx.guild.id)]

    stats = leveling.find_one({"_id": ctx.author.id})
    if stats is None:
      embed = discord.Embed(description = "You haven't sent any messages, No Rank!!")
      await ctx.send(embed=embed)
    else:
      xp = stats["xp"]
      lvl = 0
      rank = 0
      while True:
        if xp < ((50*(lvl**2))+(50*(lvl-1))):
          break
        lvl += 1


      rankings = leveling.find().sort("xp",-1)
      for x in rankings:
        rank += 1
        if stats["_id"] == x["_id"]:
          break

      embed = discord.Embed(title="{}'s Level Stats".format(ctx.author.name))
      embed.add_field(name= "Name", value= ctx.author.mention, inline=False)
      embed.add_field(name= "Level", value = f"{lvl}", inline= True)
      embed.add_field(name="Xp", value= f"{xp}/{int(((50*(lvl**2))+(50*(lvl-1))))}", inline= True)
      embed.add_field(name="Rank", value = f"{rank}/{ctx.guild.member_count}",inline=True)
      
      embed.set_thumbnail(url= ctx.author.avatar_url)

      await ctx.send(embed = embed)



  @commands.command(aliases=["top", "levels", "lb"])
  async def leaderboard(self, ctx):
    """Top Most Active users in this Guild"""


    db = cluster["leveling_guilds"]
    leveling = db[str(ctx.guild.id)]

    
    rankings = leveling.find().sort("xp",-1)
    i = 1
    embed = discord.Embed(title="Rankings")
    for x in rankings:
      try:
        temp = ctx.guild.get_member(x["_id"])
        tempxp = x["xp"]
        embed.add_field(name= f"{i}: {temp.name}", value = f"Total XP : {tempxp}", inline=False)
        i += 1
      except:
        pass
      if i == 11:
        break
    await ctx.channel.send(embed=embed)


          
  @commands.command()
  @commands.has_permissions(administrator= True)
  async def xpreset(self, ctx, user:discord.Member=None):
    """Reset the level of any user"""


    db = cluster["leveling_guilds"]
    leveling = db[str(ctx.guild.id)]

    if not user:
      await ctx.send("Mention the User!")
    stats = leveling.find_one({"_id": user.id})
    if stats is None:
      await ctx.send("The mentioned user already has no Xp!")
    else:  

      leveling.update_one({"_id" : user.id}, {"$set":{"xp":100}})

      await ctx.send(f'Successfully Reset Xp of **{user.name}**')


  @commands.command()
  @commands.has_permissions(administrator=True)
  async def setxp(self, ctx, user:discord.Member=None, xp:int=None):
    """Set Xp of a user!"""


    db = cluster["leveling_guilds"]
    leveling = db[str(ctx.guild.id)]

    if not user:
      await ctx.send("Mention the user")
    if not xp:
      await ctx.send("Specify the Xp1")
    #if xp is not int:
      #await ctx.send("The xp should be an integer")
    else:  
      stats = leveling.find_one({"_id": user.id})
      leveling.update_one({"_id": user.id}, {"$set":{"xp":xp}})
      await ctx.send(f"Xp has been set to {xp}")

    



  

#Custom help commands
  @commands.command(aliases=["level.config", "leveling.config", "levels.config"])
  @commands.cooldown(2, 200, BucketType.user)
  @commands.cooldown(2, 200, BucketType.guild)
  async def leveling(self, ctx):
    db = cluster["paradox"]
    g_configs = db["guild_configs"]
    parameters = ["No_Xp_Channels", "Xp_Rate", "Level_Roles_ID", "Level_Roles_At"]
    parameters_values = []

    g_dict = g_configs.find_one({"_id": ctx.guild.id})
    if g_dict is None:
      #ctx.invoke("guild_configs_reset")  #insert in this function too
      pass
    else:
      for para in parameters:
        para = g_dict["leveling"][str(para.lower())]
        parameters_values.append(para)


      config_embed = discord.Embed(
        color = 0x000
      )
      for i in range(len(parameters)):
        config_embed.add_field(name= parameters[i].replace("_", " "), value= parameters_values[i])
      
      config_embed.add_field(name= "Commands", value= "List of Commands that can be performed")
      config_embed.add_field(name= "This Message will no longer respond to any input in:", value = "datetime.datetime.utcnow() + timedelta of timeout minuite -- convert to discord supported UNIX TIMESTAMP FOR EASIER ACCES AND TIMER")

















                                                        # rate, per, BucketType



    




#-----------------------------------------------------------------------
def setup(client):
  client.add_cog(levels(client))






