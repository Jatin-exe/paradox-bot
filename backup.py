import json
import discord
from discord.ext import commands
import datetime
import os
from pymongo import MongoClient


cluster = MongoClient("mongodb+srv://db:databaseuser@paradox.n7mew.mongodb.net/paradox?retryWrites=true&w=majority")
db = cluster["paradox"]
b_data = db["backups"]

class backup(commands.Cog):
    """Backup- Messages, Channels , Server, State of a Server"""
    def __init__(self, client):
        self.client = client

#maybe the big daddy of backup all messages and exact ditto server state and get it back , but to do t first predict the resources that will be use , limitation on how bakc they can go , they can specifysince when messages they want to show,  
#messages bakcup


    @commands.command()
    @commands.has_permissions(administrator= True)
    async def backupm(self, ctx, days:int=10, messages:int = 100):
        if ctx.author.guild is None:
            await ctx.send("This command cant work in Dms!") #A way to do this more efficentl y for a set no of commands and categories
            return
        #CHECK SLOWDOWN OR RATELLIMITION

        #CHECKING IF THE OPERATION IS SAFE ENOUHG TO DO WITH THE RESOURCES

        #set limits based on days entered and no of messages availabe
        #if days > 30:
            #await ctx.send("No no u cant do that")
            #return #CHANGE THIS ACCRODING TO THE AMOUNT OF RESOURCES IT WILL BE SPENT ON DOING THS OPERATION AND THIS OPERATION WILL BE HEAVILY RATE LIMITED , LIKE SUPER HEAVY RATE LIMITION , BASED ON MEMBER , GUILD AND THE TYPE OF BACKUP

        t_date = datetime.datetime.utcnow()
        t_delta = datetime.timedelta(days=days, )
        target_date = t_date - t_delta



        #can we find the length of async iterator wihout using the computational power and finidgn the no of messages
        msges_list = []
        #ALWAYS GET MESSAGESF FROM TOP / IE FROM OLDEST TO NEWEST
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

            msg["Message"]["created_at"] = str(m_obj.created_at) #IMP DO THIS

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
        msges_list.append({"Guild Name": ctx.guild.name, "Guild id": ctx.guild.id})

        backup_obj = {
            "guild_id": ctx.guild.id,
            "user_id": ctx.author.id,
            "backup_time": datetime.datetime.utcnow(),
            "backup": msges_list
        }

        #LIMIT ON HOW MANY BACKUPS A PERSON CAN HAVVE AND HOW LONG THEY CAN KEEP IT IN CLOUD AND HOW OFTEN THEY CAN BACKUP
        b_list = b_data.find({"user_id": ctx.author.id})
        if len(b_list) < 5:
            b_data.insert_one(backup_obj)
        else:
            await ctx.send("Limit for Backup Storage is 5 and its full, so we couldnt backup on cloud")

        with open("/home/ubuntu/Jsons/plx_backup.json", "r")as f:
            backup_data = json.load(f)

        if str(ctx.guild.id) in backup_data:
            await ctx.send("Guild found")
        else:
            backup_data[str(ctx.guild.id)] = {}

        
        backup_data[str(ctx.guild.id)][str(datetime.datetime.utcnow())] = msges_list

        date = datetime.datetime.now()
        
        file_name = f"backup-{date.strftime('%Y%m%d-%f')}.json" 

        with open(f"/home/ubuntu/Jsons/{file_name}", "w")as f:
            json.dump(backup_data, f, indent=2)

        await ctx.send(file= discord.File(f"/home/ubuntu/Jsons/{file_name}"))

        with open("/home/ubuntu/Jsons/plx_backup.json", "w")as f:
            json.dump(backup_data, f, indent=2)


        filePath = 'f"/home/ubuntu/Jsons/{file_name}"'

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



    @commands.command()
    async def poof(self, ctx, msg:discord.Message):
        att = msg.attachments[0]
        content = await att.read()
        await ctx.send(len(content))

        text_f = open("/home/ubuntu/Jsons/text.txt", "x")
        text_f = open("/home/ubuntu/Jsons/text.txt", "w")
        text_f.write(str(content))
            
        await ctx.send(msg.attachments)
        await ctx.send(msg.attachments[0])





#----------------------------------------------------------------------
def setup(client):
    client.add_cog(backup(client))




