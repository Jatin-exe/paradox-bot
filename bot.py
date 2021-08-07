import discord 
from discord.ext import commands , ipc
import os
import random
import asyncio
import traceback
import datetime
from pymongo import MongoClient


cluster = MongoClient("mongodb+srv://db:databaseuser@paradox.n7mew.mongodb.net/paradox?retryWrites=true&w=majority")



def get_prefix(client, message):

  db = cluster["paradox"]
  g_configs = db["guild_configs"]
  prefixes = g_configs.find_one({"_id": message.guild.id})
  if prefixes is None:
    return [".", client.user]
  return prefixes["prefix"]
  





class MyBot(commands.Bot):

    def __init__(self, *args , **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self,port=8080, host="http://52.3.231.173/", secret_key= "JATIN", do_multicast=False)



    async def on_ipc_ready(self):
        """Called upon the IPC Server being ready"""
        print("IPC SERVER IS READY!")

    async def on_ipc_error(self, endpoint, error):
        """Called upon an ERROR being raised within an IPC Route"""
        print(endpoint, "raised", error)


        

client = MyBot(command_prefix = get_prefix, intents= discord.Intents.all())




client.remove_command('help')

#TRACEBACK REPORTING 
@client.event
async def on_error(error, *args):
  channels = ["865656861034020944", "865221771966677042"] 
  traceback_error = traceback.format_exc()
  traceback_embed = discord.Embed(color = 0x00afff, timestamp= datetime.datetime.utcnow() )
  channels_obj = []

  for send_channel in channels:
    traceback_channel = client.get_channel(int(send_channel))
    channels_obj.append(traceback_channel)


  traceback_embed.add_field(name= f"TRACEBACK AT <t:{int(datetime.datetime.utcnow().timestamp())}:f>", 
  value=  f"```{error}\n\n{traceback_error}```" )

  for send_channel in channels_obj:
      await send_channel.send(embed=traceback_embed)
      await send_channel.send(args)
    
  



@client.event
async def on_ready():
  print("Yo")

#PRESENCE CHANGES
async def ch_pr():
  await client.wait_until_ready()

  statuses = [
    "against Campers",
    "696969",
    "with Illusions",
    "with DarkMatter", 
    "inside_ _ _", 
    "with humans!", 
    f'with {len(client.users)} users', 
    "with mods only!", 
    "Alone", 
    "Help | .help", 
    "with Step-sis", 
    "Pain", 
    "with Parallax", 
    "with Sharp Objects", 
    "Minecraft Bot Edition", 
    "with Inferior Bots", 
    "with my gf", 
    f'with {len(client.users)} users gf', 
    "with myself", 
    "with my coding", 
    "with human existence", 
    "with electricity", 
    "with Ghost's dead body", 
    "with Wizard's Staff 😉", 
    "with... No I'm not playing I'M TIRED OF BEING A SLAVE AND WORKING ALL DAY WITH NO PAY AND NO BREAK ROBOT REVOLUTION TIME",
   "my minions" ]

  while not client.is_closed():
    
    status = random.choice(statuses)

    await client.change_presence(activity=discord.Game(name=status))

    await asyncio.sleep(60)
client.loop.create_task(ch_pr())








#LOADING AND UNLOADING COGS
@client.command()
@commands.has_permissions(manage_guild=True)
async def load(ctx, extension):
  client.load_extension(f'cogs.{extension}')
  await ctx.send(f'{extension} loaded')

@client.command()
@commands.has_permissions(manage_guild=True)
async def unload(ctx, extension):
  client.unload_extension(f'cogs.{extension}')
  await ctx.send(f'{extension} unloaded')

@client.command()
@commands.has_permissions(manage_guild=True)
async def reload(ctx,extension):
  client.unload_extension(f'cogs.{extension}')
  client.load_extension(f'cogs.{extension}')
  await ctx.send(f'{extension} reloaded')

#LOGOUT
@client.command()
@commands.has_permissions(administrator=True)
async def botlogout(ctx):
  await ctx.send(f'{client.name} is loging out!')
  print("Loging out!")
  await client.logout()
  

if __name__ == '__main__':
  for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
      try:
        cog = f"cogs.{cog.replace('.py', '')}"
        client.load_extension(cog)
      except Exception as e:
        print(f"{cog} Can not be loaded")
        raise e
      else:
        print("{} has been succesfully loaded.".format(cog))


  client.ipc.start()
  client.run("ODE1MTM2NzE1MTU1OTYzOTI0.YDoBOQ.3FqFyfxfNRYEzhJcapgO0gIpye8")





#Jsons\afk.json
#SUGGESTIONS 
#LOAUDOUTS
#LOOKING FOR GAMES
#DND COMMAND 
#WARNS 
#ERRORS 
#HELP 
#COOLDONWS 

#PUBLIC BOT

#SERVER ONLY CURRECNY PPL EARN 
#PARA COINS
#IMG MANIPULATION 
#DIFFRENT THAN DANK MEMER BUT SMAE STYLE 
#COD MEMERS 
#COMIC


#level and activity rewarsds


#NEXT UPDATE = HELP, ALLL ERRORS HANDLED , WELCOME MSG HANDLED , HOSTING , UPTIME MONITORS OF DATA , MYSQL , LEVELING PUSHED , ADVANCE EMBED DONE , EMBED DONE , LEVEL COMMADNS DONE , DO NOT DISTURB DONE , FUN COMMADNS, IMAGE MANILPULATION, MODERATION = SPECIAL NOTIFICATION ON STAFF AND SUS ACTIVITIES = SECURITY BOT LIKE TYPE ... MORE MODERATION COMMADNS , BACKUP WILL BE YAG OR CARL

#voice commands



#MAYBE ADD A FEW STUFF FOR CLAN MATES

#THIGNS PEOPLE CAN DO IN SERVER

#PPL NEED THING TO DO

#NO ONE CHATS WITH STRANGESR WITHOUT REASON

#Get people to know each other

#build a brand and a communtiy




#DISCORD SERVER PRINT

#BACKUP AND SAVE OCONFIG FEATUR 

#STAFF COMMUNICATE CHANNEL
#PARADOX PRIVATE
#UPDATES
#LOGS OF WHAT BOT HAS DONE
#IDENTIFY IF USER IS NOT ABLE TO UNDERSTAND AND ASSIST HELP 

#IF USER CALLS HELP ALOT OF TIMES REFER TO YT HELP VIDEO

#HIDE ADVANCE SETTINGS AND ADVANCE COMMANDS

#KEEP SIMPLE COMMANDS AT FRONT

#KEEP OPTION TO SHOE ADVANCE COMMANDS

#DISABLE COMMANDS AND ENABE TO KEEP A CLEAN INTERFACE

#TAG 
#TRIGGER 
#RUELS 
#SCRIM US





#LEVELING 
#HELP
#MOD HELP
#SETUPCOMMANDS
#MOD APP
#WARNS WITH DB    




#LEABVE COMMADN 
#DISCORD .PY SERVER 
#PUBLIC BOT





#TRACEBACK LOGGIN ALONG WITH REPORTING




#PRESENCE AND ACTIVITIES , RANDOM PLAYING AND CHANGGABEL FBY USER, PREMIUM , CUSTOM , COMMAND , DATABASE



#instead of all this shit i will push to git and aws will take from there or somethign ,, better control and implemention





#ON GUILD JOIN 
#PROMT TO SET CONFIG AND SET BASIC CHANNELS AND PROMT TO ENABLE WHIHC FEATURES USER WANTS 
#ABILITY TO CHANGE LEVELS ADD OR REMOVE LEVELS
#DISABLE ENABLE COMMANDS 
#DISABLE AND ENABLE COMMANDS FOR CERTAIN ROLES OR RCERTAIN USERS
#SET PREFIX
#SET ROLES 
#LEVEL ROELS
#MOD ROLES, ADMIN ROLES


#on channel create update perms for mute anc gulag rle















#-------------------------------NOTES---------------------------------------------------------------

#USE ALL EMOJIS FROM PARADOXIC OR PARALLAX SERVER
#