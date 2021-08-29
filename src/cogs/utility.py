import discord 
from discord.ext import commands
import asyncio
import datetime

from discord.ext.commands.cooldowns import BucketType


class utility(commands.Cog):
  """Useful commands"""
  def __init__(self, client):
    self.client = client




  
#EMBED BASIC
  @commands.command(aliases=["sendembed"])
  @commands.cooldown(1,45, BucketType.user)
  @commands.has_permissions(manage_messages=True)
  async def embed(self, ctx, channel:discord.TextChannel=None, color="#00afff", *, text):
    """Send a basic embed without any Images required"""
    if color.startswith("#"):
      color = color.replace("#", "0x")

    if channel is None:
      channel = ctx.channel
  
    send_embed= discord.Embed(
      description = text,
      color = color
      )

    await channel.send(embed = send_embed)
    await ctx.send("Embed Sent!", delete_after= 2)


#AVATAR 
#SIZE OF AVATAR TO BE CONSTANT OR NOT
  @commands.command(name='Avatar', aliases=["avatar", "av", "AV", "Av"])
  async def av(self,ctx, avatar_user : discord.Member=None):
    """Flex and see those Avatars!"""
    if not avatar_user is None:
      av_embed = discord.Embed(title = f'**{avatar_user.name}\'s Avatar!**',
      Color = discord.Color.blue())

      av_embed.set_image(url = avatar_user.avatar_url)

      await ctx.send(embed = av_embed)

    if avatar_user is None:
      avatar_user = ctx.author  

      av_embed = discord.Embed(title = f'**{ctx.author.name}\'s Avatar!**',
      Color = discord.Color(0x0000ff))

      av_embed.set_image(url = ctx.author.avatar_url)

      await ctx.send(embed = av_embed)

#INFO 
#MORE DETATILS IN INFO AND AVAILBE TO STAFF ONLY I THINK
#AGE ANDNICKNMAES DETAILS 
#Databasse or JsON
  @commands.command(name='info', aliases=["whois", "Whois", "Info"])
  async def info(self, ctx, info_user : discord.Member=None):
    """Get info about a user"""
    if not info_user is None:
      info_embed = discord.Embed(
        title="{}\'s Info".format(info_user.name),
        timestamp = ctx.message.created_at,
        color = discord.Color.blue()
      )

      info_embed.set_thumbnail(url = info_user.avatar_url)
      info_embed.set_footer(text= f'Requested by {ctx.author}', icon_url = ctx.author.avatar_url)

      info_embed.add_field(name="**ID**", value= info_user.id)
      info_embed.add_field(name= "**Account Created at:**", value= info_user.created_at.strftime("%a, %#d %B %Y"))
      info_embed.add_field(name= "**Server Joined at:**", value= info_user.joined_at.strftime("%a, %#d %B %Y"))

      await ctx.send(embed = info_embed)
    if info_user is None:
      info_user = ctx.author
      info_embed = discord.Embed(
        title="{}\'s Info".format(info_user.name),
        timestamp = ctx.message.created_at,
        color = discord.Color.blue()
      )

      info_embed.set_thumbnail(url = info_user.avatar_url)
      info_embed.set_footer(text= f'Requested by {ctx.author}', icon_url = ctx.author.avatar_url)

      info_embed.add_field(name="**ID**", value= info_user.id)
      info_embed.add_field(name= "**Account Created at:**", value= info_user.created_at.strftime("%a, %#d %B %Y"))
      info_embed.add_field(name= "**Server Joined at:**", value= info_user.joined_at.strftime("%a, %#d %B %Y"))

      await ctx.send(embed = info_embed)

#ADVANCE INTERACTIVE EMBED

#ask wheter to add fields 
#edit embed 
#copy json of embed
#send embed by json
#add al argumnets 
#ask all argumetns 
#mention argumnets in command if want to cancel any like the one i yagpdb

  @commands.command(Name="AdvEmbed", aliases=["advembed", "proembed", "ADVEMBED", "Advembed"])
  async def adv_embed(self, ctx):
    """An Advanced Interactive setup where you can send embeds with images and much more"""
    await ctx.send("Let's start with the Embed Process! Mention these parameters within 30 sec")

    basic_parameters = ["**Mention the Channel you want the embed to be sent in!**",
    "**The Color for the Embed? in hex (#ffffff) format only**",
    "**Title of the Embed?**",
    "**Description of the Embed**",
    "**Send an image for the embed! (in url form only)**"
    ]

    ans_basic_parameters = []

#adv embed  (tick for multiple options of react)
#Which Channel do u want to send ur mebed in ? ( tHIS , Other)
#what type of images do you want to add in ur embed ( image preview examples with name) ( thumbnail , image ) (react to the msg) 
    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel


    for i in basic_parameters:
      await ctx.send(i)

      try:
        msg = await self.client.wait_for('message',  timeout=100.0, check= check)
      except asyncio.TimeoutError:
        await ctx.send("You did not answer in time, please be quicker next time!")
        return
      else:
        ans_basic_parameters.append(msg.content)


    try:
      c_id = int(ans_basic_parameters[0][2:-1])
    except:
      await ctx.send(f'You did not mention the channel properly, do it like this {ctx.channel.mention} next time!')
      return

    advembed_send_channel = self.client.get_channel(c_id)

    advembed_color = ans_basic_parameters[1]

    if advembed_color.startswith('#'):
      await ctx.send("Color was mentioned successfully")
      advembed_color = advembed_color.replace("#", "0x")
      await ctx.send(advembed_color)
    else:
      await ctx.send("The color was not mentioned in hex format do it again")

    
    advembed_title = ans_basic_parameters[2]

    advembed_description = ans_basic_parameters[3]



    advembed_image = ans_basic_parameters[4]



    send_advembed = discord.Embed(
      title = advembed_title,
      description = advembed_description,
      color = discord.Colour(int(advembed_color, 16))
      )
    
    send_advembed.set_image(url = advembed_image)
    send_advembed.set_footer(text= send_advembed.Empty)

    await advembed_send_channel.send(embed = send_advembed)
    

  # @commands.command()
  # async def refembed(self, ctx):
  #   ref_embed = discord.Embed(
  #     title = "Title",
  #     description= "Description of the Embed\n Max is 2048 Characters ",
  #     color = 0x00aaff,
  #     url= "https://imgur.com"
  #   )

  #   ref_embed.add_field(name= "Field 1 (limit= 1024 Characters)", value="Field 1 Value (limit=2048 Characters)")
  #   ref_embed.add_field(name= "Field 2 (limit= 1024 Characters)", value="Field 2 Value (limit=2048 Characters).....")
  #   ref_embed.add_field(name= "More Info on Limits from Discord Official Docs", value="https://discord.com/developers/docs/resources/channel#embed-limits")
    

  #   ref_embed.set_author(name="Author Name")

  #   #https://media.discordapp.net/attachments/817288748995575837/859529930638360576/logo.png

  #   #https://media.discordapp.net/attachments/817288748995575837/859529968560111626/image.png?width=797&height=434
  #   ref_embed.set_image(url="https://media.discordapp.net/attachments/817288748995575837/859529930638360576/logo.png")
  #   ref_embed.set_thumbnail(url="https://media.discordapp.net/attachments/817288748995575837/859529968560111626/image.png?width=797&height=434")

  #   await ctx.send(embed=ref_embed)      


#--------------------------------------------------------------------------
def setup(client):
  client.add_cog(utility(client))
