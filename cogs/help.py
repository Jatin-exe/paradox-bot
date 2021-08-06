import discord
from discord.ext import commands


#Better help when going public
#Database to store data on help useage and stats , so we can imporve help 
#a way to make the help embed as easy as possible using ai and ml
#dashboard intgration



class help(commands.Cog):
  """Shows this Page!"""
  def __init__(self, client):
    self.client = client
#HELP COMMAND PAGE FOR MODERATORS AND HELP COMMAND PAGE FOR ADMINS AND OTHER STUFF
  
  @commands.command(aliases=["help", "HELP", "Help"])
  async def helpme(self, ctx, *cog):
    if not cog:
      cog_desc = ''
      embed = discord.Embed(color = 0x00ff00)
      for x in self.client.cogs:
        if x != "help" and "levelingsys" and "bot_stuff":
          cog_desc += f"**{x.capitalize()}** - {self.client.cogs[x].__doc__.capitalize()}\n\n"
      value = f"\n\n{cog_desc[0:len(cog_desc)-1]}"    
      embed.add_field(name= 'Commands list',value = value ,
      inline = False)
      embed.set_footer(text= "Type .help Category for more info on a command")
      await ctx.message.add_reaction(emoji ="✅")
      await ctx.send(embed = embed)
     
    
    else:
      if len(cog) > 1:
        embed = discord.Embed(
          title= "Error",
          description= "Mention only one Category or Command at a time!",
          color = 0x00ff00)
        await ctx.send(embed = embed)

      else:
        found = False
        for x in self.client.cogs:
          for y in cog:
            if x == y:
              embed = discord.Embed(color = 0x00ff00)
              scog_info = ''
              for c in self.client.get_cog(y).get_commands():
                if not c.hidden:
                  scog_info += f"**{c.name}** - {c.help}\n"

              embed.add_field(
                name= f"{cog[0]} Module",
                value = scog_info
                )
              embed.set_footer(text= "Type .help Command for more info on a command")
              found = True

        if not found:
          for x in self.client.cogs:
            for c in self.client.get_cog(x).get_commands():
              if c.name == cog[0]:
                if not c.hidden:
                  embed = discord.Embed(color = 0x00ff00)
                  embed.add_field(
                    name= f"{c.name} - {c.help}",
                    value = f"**Proper Syntax:**\n{c.qualified_name} {c.signature}\n\n**Aliases:**\n{c.aliases}"
                  )
                found=True
              #if the command mentioned is not there then | NOT WORKING RN FIX LATER 
              #else:
                #embed = discord.Embed(
                  #description =f"{c} is not a valid category or command!",
                  #color = 0x00ff00)
                #found = True
              found = True 

        await ctx.message.add_reaction(emoji ="✅")        
        await ctx.send(embed = embed)
        found = True
            


              





      #embed.add_field(name = "Command Categories!",
      #value = "**Leveling** - Commands to see level")
      #embed.add_field(name = "Command Categories!",
      #value = "**Leveling** - Commands to see level")



























#--------------------------------------------------------------------------
def setup(client):
  client.add_cog(help(client))