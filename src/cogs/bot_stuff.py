import discord
from discord.ext import commands
import datetime
import traceback


class bot_stuff(commands.Cog):
    """View Shit about Bot and do with Bot, Stats , Graphs , growth bot dev commands"""
    def __init__(self, client):
        self.client = client




        

#BASIC ERROR HANDLING
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        else:
            try:
                if hasattr(ctx.command, 'on_error'):
                    return
                else:
                    error_embed = discord.Embed(
                    title = f"Error in {ctx.command}",
                    description = f"{ctx.command.qualified_name} {ctx.command.signature} \n{error}",
                    color = 0x43780)
                    await ctx.send(embed=error_embed)
            
            except: 
                error_embed = discord.Embed(
                    title = f"Error in {ctx.command}",
                    description = error,
                    color = 0x43780
                    )
                await ctx.send(embed= error_embed)




#SHIT STUFF MOD MAIL KINDA BUT REALLY NOT MOD MAIL JUST KEEPING DATA OF SHIT MSGED TO THE BOT
"""@client.event
async def on_message(message):
  if not hasattr(message.author, 'guild'):
    print("unlegit mesaaged")
    wiz_id = "629608680752676865"
    jatin_id = "813674143961972786"

    wiz_id = client.get_user(int(wiz_id))
    jatin_id = client.get_user(int(jatin_id))

    dm_embed = discord.Embed(
      color = 0x00afff,
      timestamp= message.created_at
    )
    dm_embed.add_field(name= message.author.name + message.author.discriminator, value= message.content)
    dm_embed.set_footer(text=f"ID: {message.author.id}")
    await wiz_id.send(embed = dm_embed)
    await jatin_id.send(embed =dm_embed)
  else:
    return"""

















#----------------------------------------------------------------------
def setup(client):
  client.add_cog(bot_stuff(client))
