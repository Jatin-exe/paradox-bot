import discord 
from discord.ext import commands
import json
import asyncio
from pymongo import MongoClient






cluster = MongoClient("mongodb+srv://db:databaseuser@paradox.n7mew.mongodb.net/paradox?retryWrites=true&w=majority")


db = cluster["paradox"]
g_configs = db["guild_configs"]



channels = ["No_Xp_Channels","Mute_Channel", "Suggestion_Channel", "Starboard_Channel", "Announcements_Channel"]
roles = ["Mod_Role", "Admin_Role", "Muted_Role"]



class config(commands.Cog):
  """Change the Configuration of the bot"""
  def __init__(self, client):
    self.client = client





      
#SETUP ON GUILD JOIN
  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    guild_obj = {
        "_id": guild.id,
        "prefix": ".",
        "roles": {},
        "channels": {},
        "leveling": {},
        "moderation": {},
      }
    if g_configs.find_one({"_id": guild.id}) is None:
      g_configs.insert_one(guild_obj)
    else:
      g_configs.update_one(guild_obj)
      



#CHANGE PREFIX
  @commands.command(aliases=["change prefix", "prefix"])
  @commands.has_permissions(administrator = True)
  async def changeprefix(self, ctx, prefix):
    """Change the Prefix of the bot"""
    if prefix is None:
      await ctx.send("Correct Usage is ```.prefix <new_prefix>```")
    if len(prefix) > 3:
      await ctx.send("Prefix should not be more then 3 characters, please try again!")

    g_configs.update_one({"_id": ctx.guild.id}, {"$set" : {"prefix": str(prefix)}})    

    await ctx.send(f"Prefix changed to **{prefix}**")



#SETUP BASIC CHANNELS
  @commands.command(aliases = ["updatechannels", "setupchannel"])
  @commands.has_permissions(administrator=True)
  async def setupchannels(self, ctx):
    """An Advanced Interactive setup where you can set diffrent Channels"""
#SKIP REACTION NOT CANCAEL

    guild = ctx.guild
    basic_channels_q = []
    ans_basic_channels = []

    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel

    def check_reaction(reaction, user):
      return reaction.message.id == msg.id and user == ctx.author and str(reaction.emoji) == "❌"


    config_data = g_configs.find_one({"_id": ctx.guild.id})
    if config_data is None:
      guild_obj = {
        "_id": ctx.guild.id,
        "prefix": ".",
        "roles": {},
        "channels": {},
        "leveling": {},
        "moderation": {},
      }
      
      g_configs.insert_one(guild_obj)      

    await ctx.send("Lets Start the interactive Setup")
    for ch in channels:
      basic_channels_q.append(f"Mention the {ch}")


    for i in basic_channels_q:
      check_loop = "0"
      while check_loop == "0":
        send_embed = discord.Embed(
          color = 0x00afff
        )
        send_embed.add_field(name= i.replace("_", " ") , value= "Click on ❌ if you dont want to add this channel")
        msg = await ctx.channel.send(embed = send_embed)
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
              if i ==0:
                ans_basic_channels.append(stuff.content.channel_mentions)
              else:
                if stuff.content.startswith('<#') and stuff.content.endswith('>'):
                  ans_basic_channels.append(str(stuff.content))
                  check_loop = "1"                                  

            elif isinstance(stuff, tuple):
              add_channel = None
              ans_basic_channels.append(str(add_channel))
              check_loop = "1"

            else:
              await ctx.send(f"Please Mention the Channel properly, like this {ctx.channel.mention}")

        for future in pending:
          future.cancel()

    channels_obj = {}
    for i in range(len(ans_basic_channels)):
      channels_obj[str(channels[i].lower())] = ans_basic_channels[i]
    g_configs.update_one({"_id": ctx.guild.id}, {"$set" : {"channels" : channels_obj}})


    #SENDING THE FINAL EMBED
    finish_embed = discord.Embed(
      color = 0x00afff)
    finish_embed.add_field(name = "Finished Configuration of Channels", value= "use the command `.config` to see the Configuration of this Server Settings")

    await ctx.send(embed = finish_embed)




#SETUP BASIC ROLES
  @commands.command()
  @commands.has_permissions(administrator=True)
  async def setuproles(self, ctx):
    """An Advanced Interactive setup where you can set diffrent Roles (ie: Mod Role, Mute Role)etc"""
    guild = ctx.guild
    ans_basic_roles = []
    basic_roles = []

    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel

    def check_reaction(reaction, user):
      return reaction.message.id == msg.id and user == ctx.author and str(reaction.emoji) == "❌"


    config_data = g_configs.find_one({"_id": ctx.guild.id})
    if config_data is None:
      guild_obj = {
        "_id": ctx.guild.id,
        "prefix": ".",
        "roles": {},
        "channels": {},
        "leveling": {},
        "moderation": {},
      }
      g_configs.insert_one(guild_obj)  


    await ctx.send("Lets Start the interactive Setup")
    for rl in roles:
      basic_roles.append(f"Mention the {rl}")


    for i in basic_roles:
      check_loop = "0"
      while check_loop == "0":
        send_embed = discord.Embed(
          color = 0x00afff
        )
        send_embed.add_field(name= i.replace("_", " ") , value= "Click on ❌ if you dont want to skip this role")
        msg = await ctx.channel.send(embed = send_embed)
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
            if isinstance(stuff, discord.message.Message) and stuff.content.startswith('<@&') and stuff.content.endswith('>'):
              add_role = stuff.content
              ans_basic_roles.append(str(add_role))
              check_loop = "1"

            elif isinstance(stuff, tuple):
              reaction, user = stuff
              add_role = None
              ans_basic_roles.append(str(add_role))
              check_loop = "1"

            else:
              await ctx.send(f"Please Mention the Role properly!")

        for future in pending:
          future.cancel()




    roles_obj = {}
    for i in range(len(ans_basic_roles)):
      roles_obj[str(roles[i].lower())] = ans_basic_roles[i]
    g_configs.update_one({"_id": ctx.guild.id}, {"$set" : {"roles" : roles_obj}})


    #SENDING CONFIMATION EMBED    
    finish_embed = discord.Embed(
      color = 0x00afff
    )
    finish_embed.add_field(name = "Finished Configuration of Roles", value= "use the command `.config` to see the Configuration of this Server Settings")

    await ctx.send(embed = finish_embed) 


  @commands.command(aliases=["Config", "configuration"])
  async def config(self, ctx):
    config_data = g_configs.find_one({"_id": ctx.guild.id})
    if config_data is None:
      pass

  #GETTING THE REGISTERED CHANNELS
    ch_list = []
    for ch in channels:
      ch_id = config_data["channels"][ch.lower()]
      if ch_id == "None":
        ch_id = "This Channel is not specified"
      ch_list.append(ch_id)


    rl_list = []
    for rl in roles:        
      rl_id = config_data["roles"][rl.lower()]
      if rl_id == "None":
        rl_id = "This Role is not specified"
      rl_list.append(rl_id)
  

        

    



    embed_channels_value = ""    
    for i in range(len(ch_list)):
      embed_channels_value += f"{channels[i]} : {ch_list[i]}\n" 


    embed_roles_value = ""    
    for i in range(len(rl_list)):
      embed_roles_value += f"{roles[i]} : {rl_list[i]}\n" 


    config_embed = discord.Embed(
      title = f"{ctx.guild.name}\'s Configuration",
      color = 0x00afff,
    )


    config_embed.add_field(
      name="Channels",
      value= embed_channels_value,
      )

    config_embed.add_field(
      name= "Roles",
      value= embed_roles_value,
      )

    await ctx.send(embed= config_embed)


  @commands.command()
  @commands.has_permissions(administrator=True)
  async def leave(self, ctx, *, reason=None):
    def check_reaction(reaction, user):
      return reaction.message.id == bot_msg.id and user == ctx.author and str(reaction.emoji) == "✔️"

    bot_msg = await ctx.send("Are you sure you want me to leave the Guild?")
    await bot_msg.add_reaction(emoji= "✔️") 

    try:
      reaction_value = await self.client.wait_for('reaction',  timeout=40.0, check= check_reaction)
    except asyncio.TimeoutError:
      await ctx.send("You did not answer in time, please be quicker next time!")
      return
    else:
      await ctx.guild.leave()


#ROLES BASIC ROLES 
#ENABLE AND DISABLE COMMADNDS


    

    #CHANNELS
    #DISABLED COMMANDS AND ENABLED COMMANDS
    #SET ADMIN MOD ROLES AND MAYBB OTHER ROELS 
    #SERVER MEMBERS CHANNEL SET
    



#noxp command
#add to no xp



# ENABLE DISABLE COMMADNS AND ADV COMMADNS EVEN WITH CATEGORIES




#MEMBER CHANNEL ------------------------------------------
  @commands.Cog.listener()
  async def on_member_join(self, member):
    asyncio.sleep(5*60)
    guild = member.guild

    for stats_channel in guild.channels:
      if stats_channel.name.startswith('All Members:'):
        await stats_channel.edit(name=f'All Members: {guild.member_count}')
        break 




#----------------------------------------------------------------------
def setup(client):
  client.add_cog(config(client))



#FUCK U MORTY JUST FUCK FUCKING UAND GET THE FUCK OUT OF HERE BEFORE I GET SERIOUS AND JUST FUCK EVERHTHIBG THAT U KNOW ABOT WORLD UP JUST GET THAT SHIT IN UR BARINA  MANN JUST GET IT IN UR BRAINS RIGHT U GET THAT SHIT OR NO TELL MAN RO I AM GONN FUCK U REAL HARD SO HARD THAT EVEN THE BADDES SHIT WONT BE ABLE TO UNDO IT AND U KNOW WHA I MEAN EHWNE I SAY THE BADDEST MEA  I HPE UGET THAT SHIT RIGHT AND NOT BE A FUCKING LOSER AND A ASS HOLE LIEK THEON U ALWASY ARE SAND JUST GE TTHIS THING UIN UUR BRAIN IN THE WAY THT THAT ALWSY WIL BE THERE 