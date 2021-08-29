import discord
from discord.ext import commands, tasks
from pymongo import MongoClient
import dns
import json
import asyncio


def convert_time(time):

  pos = ["s", "m", "h", "d"]

  time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d" : 3600 * 24}

  unit = time[-1]

  if unit not in time_dict:
    return -1

  try : 
    val = int(time[:-1])
  except:
    return -2
  
  return val * time_dict[unit]


from dotenv import dotenv_values
VALUES = dotenv_values("paradox-bot/venv/.env")
cluster = MongoClient(VALUES["DB_URI"])


def check_high(mod, member):  
  if mod.top_role <= member.top_role:
    return False

class moderation(commands.Cog):
  """Moderating Commands"""
  def __init__(self, client):
    self.client = client


#IGNORE COMMAND 
HAB TO DO THIS

ON GUILD JOIN IN CONFIG
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.channel == media_channel:
      if message.attachments is None:
        await message.delete()


  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def kick(self, ctx, user:discord.Member=None, *, reason=None):
    """Kicks a User from the Guild"""
    if not user:
      await ctx.send("Mention the user you want to kick")
      return    
    if not reason:
      await ctx.send("Provide a reason for the kick!")
      return
    if check_high(ctx.author, user) is False:
      await ctx.send("You are not HIGH enough to do that!")
      return

    reason = f"kicked by {ctx.author.name}, Reason: {reason}"
    try:
      await self.client.send_message(user, f"You have been kicked from {ctx.guild.name}")
      await user.kick(reason=reason)
      await ctx.send(f"**{user.name}** has been kicked! by {ctx.author.name}")
    except:
      await user.kick(reason=reason)
      await ctx.send(f"**{user.name}** has been kicked! by {ctx.author.name}")
      

  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def ban(self, ctx, user:discord.Member=None, *, reason=None):
    """Bans a User from the Guild"""
    if not user:
      await ctx.send("Mention the user you want to Ban")
      return    
    if not reason:
      await ctx.send("Provide a reason for the Ban!")
      return
    if check_high(ctx.author, user) is False:
      await ctx.send("You are not HIGH enough to do that!")
      return
  
    reason = f"Banned by {ctx.author.name}, Reason: {reason}"
    try:
      await self.client.send_message(user, f"You have been Banned from {ctx.guild.name}")
      await user.ban(reason=reason)
      await ctx.send(f"**{user.name}** has been Banned! by {ctx.author.name}")
    except:
      await user.ban(reason=reason)
      await ctx.send(f"**{user.name}** has been Banned! by {ctx.author.name}")    
    return



  @commands.command()
  @commands.has_permissions(ban_members=True)
  async def unban(self, ctx, *, member):
    """Unban a Person, format:- User#tag"""

    banned_users = await ctx.guild.Bans()
    member_name, member_disc = member.split('#')

    for banned_entry in banned_users:
      user = banned_entry.user

      if(user.name, user.discriminator)==(member_name, member_disc):
        await ctx.guild.unban(user)
        await ctx.send(member_name + " has been unbanned!")
        return 
    
    await ctx.send(member + " was not found")


      
  @commands.command(aliases= ["clear"])
  @commands.has_permissions(manage_messages=True)
  async def purge(self, ctx, amount:int):
    """Delete Messages in Bulk"""
    if not amount:
      await ctx.send("Mention the amount of Messages you want to delete! Max = 100")
    amount += 1
    await ctx.channel.purge(limit=amount)
    amount -= 1
    await ctx.send(f"Purged **{amount}** Messages!", delete_after=3)
    
    #PUrge bot only or specife input user or crieteria can be fulified by an arg

#WARNINGS
  @commands.command()
  @commands.has_permissions(kick_members=True)
  async def warn(self, ctx, user:discord.Member=None, *, reason=None):
    """Warns a User"""
    if not user:
      await ctx.send("Mention the user you want to Warn")
      return    
    if not reason:
      await ctx.send("Provide a reason for the Warn!")
      return
    if check_high(ctx.author, user) is False:
      await ctx.send("You are not HIGH enough to do that!")
      return

    """async def mod_check(ctx, member):
  if not member:
    await ctx.send("Mention the User you want to warn ")
"""
    db = cluster["mod_data"]
    mod = db[str(ctx.guild.id)]

    warned_user = f'{user.name}#{user.discriminator}' 
    reason_sent = reason
    date_time = ctx.message.created_at
    date_time = str(date_time)
    date_time = date_time[:9]


    user_warns = mod.find_one({"_id": user.id})
    if user_warns is None:
      warns_no = 1
      reason_list = []
      reason_mods = []
      date_list = []
      reason_mods.append(ctx.author.name)
      reason_list.append(reason_sent)
      date_list.append(date_time)

      warned = {"_id" : user.id, "user": warned_user, "reason" : reason_list, "mod": reason_mods,"date":date_list, "warns" : warns_no}
      mod.insert_one(warned)
      await ctx.send(f"**{user.name}** has been warned, this is their first warning.")

    else:
      reason_list = user_warns["reason"]
      reason_mods = user_warns["mod"]
      warns_no = user_warns["warns"]
      date_list = user_warns["date"]
      reason_mods.append(f'{ctx.author.name}')
      reason_list.append(reason_sent)
      date_list.append(date_time)
      warns_no += 1
      mod.update_one({"_id" : user.id}, {"$set":{"user": warned_user,"warns" : warns_no, "reason":reason_list, "date" : date_list, "mod" : reason_mods }})
      await ctx.send(f"**{user.name}** has been warned,\n**Warns:** {warns_no}")
    
#CASE ID 
#WARNED BY
  @commands.command(aliases=["topwarns", "allwarns"])
  @commands.has_permissions(view_guild_insights=True)
  async def warns(self, ctx, user:discord.User=None):
    """Shows the Warns of everyone if no user is mentioned"""
    db = cluster["mod_data"]
    mod = db[str(ctx.guild.id)]

    
    if not user:
      top_warns = mod.find().sort("warns",-1)
      i = 1
      embed = discord.Embed(title="Top Warns!")
      for x in top_warns:
        try:
          temp = ctx.guild.get_member(x["_id"])
          tempwarns = x["warns"]
          embed.add_field(name= f"{i}: {temp.name}", value = f"Warns : {tempwarns}\nID: {temp.id}", inline=False)
          i += 1
        except:
          pass
        if i == 11:
          break
      await ctx.channel.send(embed=embed)
      

    if user:
      user_warns = mod.find_one({"_id": user.id})
      if user_warns is None:
        embed = discord.Embed(title = f"No Warns for **{user.name}#{user.discriminator}**", color = 0x010101)
        await ctx.send(embed = embed)
      else:
        warns_no = user_warns["warns"]
        warn_reasons = user_warns["reason"]
        warn_mods = user_warns["mod"]
        date_warned = user_warns["date"]

        embed  = discord.Embed(
          title = f'{warns_no} Warnings found',
          color = 0x010101,
          )
        for i in range(0,len(warn_reasons)):
          embed.add_field(name = f"**{date_warned[i]}**", value= f'Responsible moderator: {warn_mods[i]}\nReason: {warn_reasons[i]}') 
        embed.set_footer(text=f'{user.name}#{user.discriminator} | ID: {user.id}')
        await ctx.send(embed = embed)


    #shows the case id of warn too
    #Pagination 


  @commands.command(aliases = ["clw", "clearwarnings"])
  @commands.has_permissions(view_audit_log=True)
  async def clearwarns(self, ctx, user:discord.User=None):
    """Clear all Warnings of a Member"""
    if not user:
      await ctx.send("Mention the user")
      return

    db = cluster["mod_data"]
    mod = db[str(ctx.guild.id)]

    if user:
      user_warns = mod.find_one({"_id": user.id })
      if user_warns is None:
        embed = discord.Embed(title = f"No Warns for **{user.name}#{user.discriminator}**", color = 0x010101)
        await ctx.send(embed= embed)
      else:
        mod.delete_one(user_warns)
        embed = discord.Embed(title = f"Cleared All Warns for **{user.name}#{user.discriminator}**", color = 0x010101)
        await ctx.send(embed= embed)
    

    

  @commands.command()
  @commands.has_permissions(view_guild_insights=True)
  async def removewarn(self, ctx):
    """Clear a warning by Case id"""
    return

  @commands.command()
  async def mute_set(self, ctx, mute_role:discord.Role):
    for channel in ctx.guild.channels:
      await channel.set_permissions(mute_role, send_messages=False, add_reactions= False, speak= False)
    mute_role.edit(permissions= discord.Permissions(read_messages=True, send_messages=False, add_reactions=False, speak= False))
    
    await ctx.send("Mute perms for all channels have been reset")
    
      
  
  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def mute(self, ctx, user:discord.Member=None, time=None, *, mute_reason=None):
    """Mute a person for a specified duration"""    
    if check_high(ctx.author, user) is False:
      await ctx.send("You are not HIGH enough to do that!")
      return
    if user is None :
      await ctx.send("Please Specify the User by mentioning them")
      return

    db = cluster["paradox"]
    g_configs = db["guild_configs"]
    guild_data = g_configs.find_one({"_id": ctx.guild.id})
    #ADD GULD DATA WHEN SETTING MUTE ROLE OR MUTE CHANNEL

    try:
      mute_channel = guild_data["channels"]["mute_channel"]
    except:
      await ctx.send("Mute Channel is not set yet!\n You can set by using the command ```.mute channel```")
    try:
      mute_role = guild_data["roles"]["muted_role"]
    except:
      await ctx.send("Mute Role hasnt benn set yet!\n You can set by using the command ```.mute role```")
    
    if time is None:
      time = "12h" #Default Duration for Mute (hardcoded)

    time = convert_time(time)

    paradox_object = ctx.guild.get_member(int(self.client.user.id))

    if user.top_role >= paradox_object.top_role:
      await ctx.send("I am not high enough in the role hierarchy to that")
    
    muted_role =  ctx.guild.get_role(int(mute_role[3:-1]))
    roles_id = []
    boost_role = ctx.guild.premium_subscriber_role
  

    db = cluster["roles_taken_away"]
    rl_data = db[str(ctx.guild.id)]
    #CHECKING AND DELETING PREVIOUS LIST OF ROLE IF ANY
    rl_dict = rl_data.find_one({"_id": user.id})
    if rl_dict is not None:
      rl_data.delete_one({"_id": user.id})

    user_booster = False
    for rl_obj in user.roles:
      if rl_obj == boost_role:
        user_booster = True
      if rl_obj.id != ctx.guild.id and rl_obj.id != muted_role.id and rl_obj != boost_role:
        roles_id.append(rl_obj.id)


    rl_dict = {
      "_id": user.id,
      "roles_taken_away": roles_id
    }
    rl_data.insert_one(rl_dict)    

    if user_booster == True:
      await user.edit(roles=[muted_role, boost_role])
    else:
      await user.edit(roles=[muted_role])
    await ctx.send(f"**{user.name}** has been muted by {ctx.author.name}")

    await asyncio.sleep(time) #BAD BAFD BAD BAD BAD 

    
    if user_booster == True:
      roles_id.append(boost_role.id)
    new_roles_id = []
    for int_roles_id in roles_id:
      new_role =  ctx.guild.get_role(int_roles_id)
      new_roles_id.append(new_role)

    await user.edit(roles = new_roles_id)

    

    
    #IF NO MUTE CH OR ROLE INFORM THE STAFF
    #STAFF INFOMR CHANNLE ABOUT THE UPDATES AND SUSPICOUS ACTIVITES LGG CHANNEL 
    #STAFF ROLE PING THE STAFF ROLE FOR EMERGENCEIE 

    #NO ASYNCIO BITCH





  @commands.command(aliases=["Unmute", "UNMUTE"])
  async def unmute(self, ctx, user:discord.Member=None, *, reason=None):
    """Unmute da soul who has been muted"""
    if user is None:
      await ctx.send("Please Specify the User by Mentioning them or their idś")
    if check_high(ctx.author, user) is False:
      await ctx.send("You are not HIGH enough to do that!")
      return

    db = cluster["paradox"]
    g_configs = db["guild_configs"]
    guild_data = g_configs.find_one({"_id": ctx.guild.id})
    
    try:
      mute_channel = guild_data["channels"]["mute_channel"]
    except:
      await ctx.send("Mute Channel is not set yet!\n You can set by using the command ```.mute channel```")
    try:
      mute_role = guild_data["roles"]["muted_role"]
    except:
      await ctx.send("Mute Role hasnt benn set yet!\n You can set by using the command ```.mute role```")

    muted_role =  ctx.guild.get_role(int(mute_role[3:-1]))


    #CHECKING IF THERE IS GUILD ID IN JSON FILE
    db = cluster["roles_taken_away"]
    rl_data = db[str(ctx.guild.id)]
    rl_dict = rl_data.find_one({"_id": user.id})
    
    if rl_data is not None:
      if rl_dict is not None:
        pre_roles_id = rl_dict["roles_taken_away"]
        pre_roles_obj = []
        boost_role = ctx.guild.premium_subscriber_role


        user_booster = False
        for user_roles in user.roles:
          if user_roles == boost_role:
            user_booster = True
          
        for pre_roles in pre_roles_id:
          new_role =  ctx.guild.get_role(int(pre_roles))
          pre_roles_obj.append(new_role)

        if user_booster:
          pre_roles_obj.append(boost_role) 
        await user.edit(roles= pre_roles_obj)
        await ctx.send(f"**{user.name}** has been unmuted by " + ctx.author.name)
      else:
        await user.remove_roles(*[muted_role])
    else:
      await user.remove_roles(*[muted_role])

    rl_data.delete_many({"_id": user.id})
    
  




#----------------------------------------------------------------------
def setup(client):
  client.add_cog(moderation(client))





  # Case Id 
  #mute - Mute all channels - setup mute channel and mute role 

  #unmute
  # 
  # Help for mods and Setup
  # better Rank and leaderboard ui 
  # slow mode - per min a partuciula no of xp (leveling )/ XP rate 
  # slow mode for commands 







  # MOD HELP 

# {PREFIX} KICK 
# .BAN 
# .BAN_ID**
# .UNBAN
# .MUTE
# .UNMUTE

# .SETUPMODERATION ( INFO THAT THIS IS A CATEGORY TYPING .SETUPMODERATION OR ANYTHIGN RELATED WILL SHOW HOW TO SETU AND ADV RELATED MOD TOOL ALONG WITH LINK OT DASHBOARD OF THE MOD PANNEL)

# - MUTE ROLE


# - DELETE MESSAGES 
# - MOD LOG
# - RAID PROTECTION
# - RAID MODE 
# - SERVER LOCKDOWN
# -ANTI RAID 
# - ALERTS AND NOTIFCATIONS (SECURITY BOT)
# - AUTO MOD SETTING
# - EVERYTHING SHOULD BE ABLE TO DONE BY COMMANDS AND SIMPLE COMMAND THEY SHOULD NOT LOOK LCOMPLEX 

# -INTERACTIVE AND ADD FILTERS OF YAG -M 13232323 THINGY AND PAGINATION 
# - LINK TO HELP SERVER
# - DASHBOARD SIMPLE AND A WAY TO USE ADV COMMANDS 
# -ADV COMMANDS WILL BE HIDDEN FOR BEGINNERS SO THEY CAN UNDERSTAND THE BASIC STUFF 
# - IF HTEY WNAT THEY CAN SEE THE ADV COMMMANDS AND THEN THERE WILL BE LITERALLY NO NEED OF A CUSTOM BOT BEING MADE IT WILL  BE SO ADV THAT HUMANN MIDN SHOULD NOT BE BLE TO COMPREHEAND 
# - RESET BUTTON IF THEY MESS UP THE ADV COMMANDS AND FEATURES

