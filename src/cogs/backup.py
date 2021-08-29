import json
import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import datetime
import os
from pymongo import MongoClient

from core import *

from dotenv import dotenv_values
VALUES = dotenv_values("paradox-bot/venv/.env")
cluster = MongoClient(VALUES["DB_URI"])

         

db = cluster["paradox"]
b_data = db["backups"]

class backup(commands.Cog):
    """Backup- Messages, Channels , Server, State of a Server"""
    def __init__(self, client):
        self.client = client

    @commands.group() # name="backup", aliases=["Backup"], invoke_without_command=True)
    async def backup(self, ctx):
        pass


    @commands.command()
    @commands.check(no_dm)
    async def test_try(self,ctx):
        await ctx.send("hahalahahalhlah")


    @backup.command(name="text", aliases=["chatlog", "log"])
    @commands.check(no_dm)
    @commands.cooldown(2, 200, BucketType.user)
    @commands.cooldown(2, 200, BucketType.guild)
    @commands.has_permissions(administrator= True)
    async def backup_chat_log(self, ctx , days:int=10, messages:int=100):
        print(f"started at {datetime.datetime.now()}")
        print(f"started at {datetime.datetime.utcnow()}")

        #fix date and time ,,, if chosed a specifc date like after this date then no of messaegs wont come till new
        
        #ALWAYS GET MESSAGESF FROM TOP / IE FROM OLDEST TO NEWEST
        #can we find the length of async iterator wihout using the computational power and finidgn the no of messages
        t_date = datetime.datetime.utcnow()
        t_delta = datetime.timedelta(days=days)
        target_date = t_date - t_delta

        msges_list = []
        authors = {}

        async for m_obj in ctx.channel.history(after=target_date, limit = messages):

            if m_obj.author not in authors:
                authors[f"{m_obj.author.name}#{m_obj.author.discriminator}(id:{m_obj.author.id})"] = 1
            else:
                authors[f"{m_obj.author.name}#{m_obj.author.discriminator}(id:{m_obj.author.id})"] += 1

            msg = ""
            msg += f'[{str(m_obj.created_at.replace(microsecond=0))}]({m_obj.author.name}#{m_obj.author.discriminator}): ' 
            #better formate date in more human likeable way
            msg += m_obj.content
            if m_obj.edited_at:
                print("edited")
                msg += f"(edited at {m_obj.edited_at.replace(microsecond=0)})"

            if len(m_obj.attachments) > 0:
                attach_url_list = []
                for attach in m_obj.attachments:
                    attach_url_list.append(attach.url)
                msg += f' | ATTACHMENTS: {attach_url_list} '
            
            if len(m_obj.reactions) > 0:
                reaction_list = []
                for react in m_obj.reactions:
                    reaction_list.append(react.emoji)
                msg += f" | REACTIONS: {reaction_list}"

            #is edited
            msg += "\n\n"
            msges_list.append(msg)
        #authors dict keys
        msg_header = f"""

Guild Name: {ctx.guild.name}
Channel Name: {ctx.channel.name}

Messages start from: {target_date.replace(microsecond=0)} UTC
No of Messages; {len(msges_list)}

Authors ({len(authors)}) : {list(authors)} #


--------------------Chat Log--------------------


"""

        msg_footer = f"""
---------------------End------------------------

Backup Created by: {ctx.author.name}#{ctx.author.discriminator}
Backup Creation Date (UTC): {datetime.datetime.utcnow().replace(microsecond=0)}

This file is encrpyted and paradox is not responsible for privacy threats,
Backup is only allowed by Admins of a server and they are responsible for any Privacy Issues


This Chat log is created using Paradox Bot on Discord
"""

        #Loop break
        with open("text_backup.txt", "w")as f:
            f.write(msg_header)

        with open("text_backup.txt","a")as f :
            f.writelines(msges_list)

        with open("text_backup.txt","a")as f :
            f.write(msg_footer)

        await ctx.send(file= discord.File(f"text_backup.txt"))
        #create file name based on time and delete after sending
        #maybe srtore in databse ?

        print(f"Finished at {datetime.datetime.now()}")
        print(f"Finished at {datetime.datetime.utcnow()}")
        
        #how willl i handle this when bot gets bigger and suddenly there are multiple peopele making bakcup will the fiielt overwritten over and over an become corrupt and shit 
        #overwritin g a file localy might nob e best bor 


        #encrpyt this data with a secret key ... HASH it and store  it
        #which msg are they refrecning when replying 
        #embeds are not supported in this / later might do , maybe i dont wanna do it 
        #later add links to all the emojis that are being refrenced so that if they want to see what an emoji looks like they can go to header and click on link if the emoji still exists



    @backup.command(name="deep", aliases=["rich", "rich embed", "all messages"])
    @commands.cooldown(2, 200, BucketType.user)
    @commands.cooldown(2, 200, BucketType.guild)
    @commands.has_permissions(administrator= True)
    @commands.check(no_dm)
    async def backup_richly(self, ctx, days:int=10, messages:int=100):
        #change this explanation and doc lol its not leab
        """Fetches specified amount of messages and gives themcr back with a neat discord like rich embed feature which can be downloaded and viewed on webpage"""


        if ctx.author.guild is None:
            await ctx.send("This command cant work in Dms!") #A way to do this more efficentl y for a set no of commands and categories i mean here to make a global chekc or initailzied chekcs in files tnen import it and use as a property in her
            return

        #CHECK SLOWDOWN OR RATELLIMITION

        #CHECKING IF THE OPERATION IS SAFE ENOUHG TO DO WITH THE RESOURCES

        #set limits based on days entered and no of messages availabeb
        #if days > 30:
            #await ctx.send("No no u cant do that")
            #return #CHANGE THIS ACCRODING TO THE AMOUNT OF RESOURCES IT WILL BE SPENT ON DOING THS OPERATION AND THIS OPERATION WILL BE HEAVILY RATE LIMITED , LIKE SUPER HEAVY RATE LIMITION , BASED ON MEMBER , GUILD AND THE TYPE OF BACKUP

        t_date = datetime.datetime.utcnow()
        t_delta = datetime.timedelta(days=days )
        target_date = t_date - t_delta



        #ALWAYS GET MESSAGESF FROM TOP / IE FROM OLDEST TO NEWEST
        #can we find the length of async iterator wihout using the computational power and finidgn the no of messages
        msges_list = []
        authors = {}
        async for m_obj in ctx.channel.history(after=target_date, limit = messages):

            if m_obj.author not in authors:
                authors[m_obj.author.name] = 1
            else:
                authors[m_obj.author.name] += 1


            msg = {}
            
            #Author
            msg["Author"] = {}

            msg["Author"]["id"] = m_obj.author.id
            msg["Author"]["full_name"] = m_obj.author.name
            msg["Author"]["avatar"] = m_obj.author.avatar
            msg["Author"]["bot"] = m_obj.author.bot

            #Message
            msg["Message"] = {}

            msg["Message"]["id"] = m_obj.id
            msg["Message"]["content"] = str(m_obj.content)
            reactions_list = []
            for i in m_obj.reactions:
                reaction_users = []
                async for x in i.users():
                    reaction_users.append(x.name)
                reaction_tuple = (str(i.emoji), reaction_users)
                reactions_list.append(tuple(reaction_tuple))

            msg["Message"]["reactions"] = reactions_list

            msg["Message"]["created_at"] = str(m_obj.created_at.replace(microsecond=0)) 

            #MSG EMBEDS
            embed_list = []
            for e_obj in m_obj.embeds:
                e_dict = e_obj.to_dict()
                embed_list.append(e_dict)

            msg["Message"]["embeds"] = embed_list

            attachments_list = []
            for att_obj in m_obj.attachments:
                attachments_list.append(str(att_obj.read()))

            msg["Message"]["attachments"] = attachments_list





            



            
            
                        
            msges_list.append(msg)


        await ctx.send(authors)
        msges_list.append({"Guild Name": ctx.guild.name, "Guild id": ctx.guild.id, "Channel Name": ctx.channel.name})

        backup_obj = {
            "guild_id": ctx.guild.id,
            "user_id": ctx.author.id,
            "backup_time": datetime.datetime.utcnow(),
            "backup": msges_list
        }

        #LIMIT ON HOW MANY BACKUPS A PERSON CAN HAVVE AND HOW LONG THEY CAN KEEP IT IN CLOUD AND HOW OFTEN THEY CAN BACKUP
        """        b_list = b_data.find({"user_id": ctx.author.id})
        if len(b_list) < 5:
            b_data.insert_one(backup_obj)
        else:
            await ctx.send("Limit for Backup Storage is 5 and its full, so we couldnt backup on cloud")"""

        backup_data = {}
        backup_data[str(ctx.guild.id)] = {}
        backup_data[str(ctx.guild.id)][str(datetime.datetime.utcnow().replace(microsecond=0))] = msges_list

        date = datetime.datetime.utcnow().replace(microsecond=0)
        
        file_name = f"backup-{date.strftime('%Y%m%d-%f')}.json" 

        with open(f"{file_name}", "w")as f:
            json.dump(backup_data, f, indent=2)

        await ctx.send(file= discord.File(f"{file_name}"))


        filePath = 'f"{file_name}"'

        if os.path.exists(filePath):
            os.remove(filePath)
            await ctx.send("Done!", delete_after= 6)
        else:
            await ctx.send("Can not delete the file as it doesn't exists")

        #best way to find and return lenght without using resources            
        #print(length)


        






#CHAT LOG 
#ADV CHAT LOG / MESSAGES BACKUP 
#SERVER BACKUP - ROLES , CHANNELS , LIST OF MEMBERS , BANS
#DATABASE STORE 
#KEY PAIR
#send in a html format



#----------------------------------------------------------------------
def setup(client):
    client.add_cog(backup(client))




