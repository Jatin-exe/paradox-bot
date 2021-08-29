from dotenv import dotenv_values
from pymongo import MongoClient

VALUES = dotenv_values("paradox-bot/venv/.env")
cluster = MongoClient(VALUES["DB_URI"])





list_nodm_commands = ["backup deep", "backup", "deep"]

def premium_cog_command(ctx):

    pass

def private_cog_command(ctx):
    pass

async def get_prefix(msg):
    """Pass in Context only Bois"""
    db = cluster["paradox"]
    g_configs = db["guild_configs"]
    prefixes = g_configs.find_one({"_id": msg.guild.id})
    if prefixes is None:
        return "."
    return prefixes["prefix"] 
    
    #what if preifx is list or something ? give only one or what  #client .user objecet store prefix in selff.prefix how ?



def enabled(ctx):
    pass

automate_assigining_of_no_dm_commands =["?"]

async def no_dm(ctx):
    """No DM'S Pls"""
    if ctx.guild.id is None:
        await ctx.send("Hey, You can't use this command in Dm's")
        print("dmed")
    else: return True



def convert_time(time):

  pos = ["s", "m", "h", "d"]

  time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d" : 3600 * 24}

  unit = time[-1]

  if unit.lower() not in pos:
    return -1

  try : 
    val = int(time[:-1])
  except:
    return -2
  
  return val * time_dict[unit]



#every onec in a while the bot 

#has a mental breakdown

#has existensial crisis 

#behaves like marwin

#snaps at almost everythin

#becomes overly abusive 

#becomes toxic 

#these mostly happen to guilds or users who have been using the bot for a long time

#sends a cookie 

#asks someone to join their plan and betray humans to get a gift nitro or someting